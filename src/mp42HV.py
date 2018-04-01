#!/usr/bin/env python

"""
mp42hV
Yeah, this name is kinda shitty.
In case you wonder, it means "mp4 to Hidden Volume".

This script aims to produce a hybrid file from a mp4 file and a VeraCrypt
volume so that both are still readable.
"""
import sys
import array
import shutil
import logging


# Global variables
endianness = sys.byteorder
VC_MIN_SIZE = 131072
BLOCKSIZE = 65536

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level="DEBUG", format="%(asctime)s:%(name)s:%(lineno)s:%(levelname)s - %(message)s")


##### Utils
def intify(s, offset=0):
    return int(s[offset:offset + 4].hex(), 16)


def stringify(i):
    return bytes.fromhex("{:08x}".format(i))


def copy_block(src, dst, size):
    while size > 0:
        nb_bytes = size
        if nb_bytes > BLOCKSIZE:
            nb_bytes = BLOCKSIZE
        block = src.read(nb_bytes)
        if not block:
            break
        dst.write(block)
        size -= len(block)
    return size


##### Atom class
class Atom:
    def __init__(self, atom_or_file=None, offset=0, size=0):
        self.offset = offset

        if isinstance(atom_or_file, str):
            self.name = atom_or_file.decode()
            self.size = size
        else:
            atom_or_file.seek(offset)
            s = atom_or_file.read(8)

            if len(s) < 8:
                raise EOFError("End of file has been reached")

            self.size = intify(s)
            self.name = s[4:].decode()

            if not self.size:
                # got to EOF
                atom_or_file.seek(0, 2)
                self.size = atom_or_file.tell() - offset
            elif self.size == 1:
                raise ValueError("64-bit files are not handled")

        self.end = self.offset + self.size

    def __repr__(self):
        return "Atom({}, {}, {})".format(self.name, self.offset, self.size)

    def read(self, file):
        file.seek(self.offset)
        data = file.read(self.size)

        if len(data) != self.size:
            raise IOError("Unexpected end of file")

        return data

    def copy(self, srcfile, dstfile, payload_only=False, offset_adjust=0):
        if self.name == "mdat":
            offset = self.offset
            size = self.size

            if payload_only:
                offset += 8
                size -= 8
            srcfile.seek(offset)

            if copy_block(srcfile, dstfile, size):
                raise IOError("Unexpected end of file")

        elif self.name == "moov":
            moov = self.read(srcfile)
            stco_pos = 0

            while True:
                stco_pos = moov.find(b"stco\0\0\0\0", stco_pos + 5) - 4

                if stco_pos <= 0:
                    break

                stco_size = intify(moov, stco_pos)
                stco_count = intify(moov, stco_pos + 12)

                if stco_size < (stco_count * 4 + 16):
                    # wring stco size, potential false positive?
                    continue

                start = stco_pos + 16
                end = start + stco_count * 4
                data = array.array('I', moov[start:end])

                if endianness == "little":
                    data.byteswap()

                try:
                    data = array.array('I', [d + offset_adjust for d in data])
                except OverflowError:  # invalid offset
                    continue

                if endianness == "little":
                    data.byteswap()

                moov = moov[:start] + data.tostring() + moov[end:]

            dstfile.write(moov)


#####
def get_atoms(s_file):
    atoms = dict()
    relevant_atoms = ('ftyp', 'mdat', 'moov')
    other_atoms = ('free', 'wide', 'uuid')
    offset = 0

    atom = None
    while True:
        try:
            atom = Atom(s_file, offset)
        except EOFError:
            break

        if atom.name in relevant_atoms:
            if atom.name in atoms:
                raise ValueError("Duplicate {} atom".format(atom.name))
            atoms[atom.name] = atom
        elif not (atom.name in other_atoms):
            logger.error("Unknown atom {}, ignoring".format(atom.name.decode()))
        offset = atom.end

    try:
        return tuple([atoms[a] for a in relevant_atoms])
    except KeyError:
        raise ValueError("Missing %s atom".format(atom))


def embed(srcfile, dstfile):
    try:
        ftyp, mdat, moov = get_atoms(srcfile)
    except (IOError, ValueError) as e:
        logger.error("Error while parsing source file: {}".format(e))
        return 1

    if ftyp.size > (BLOCKSIZE - 8):
        raise RuntimeError("'ftyp' atom is too long")

    # copy data
    dstfile.seek(0, 2)
    eof = dstfile.tell() - VC_MIN_SIZE

    if eof <= VC_MIN_SIZE:
        raise RuntimeError("VeraCrypt volume is too small")
    dstfile.seek(eof)

    if (eof + mdat.size - 8 + moov.size) >= (2 ** 32):
        raise RuntimeError("Video file is too large (must be < 4GiB)")

    mdat.copy(srcfile, dstfile, payload_only=True)
    mdat_end = dstfile.tell()
    moov.copy(srcfile, dstfile, offset_adjust=(eof - mdat.offset - 8))

    # Overwrite file header to have that of a mp4 file
    head = ftyp.read(srcfile) + b"\0\0\0\x08free"
    head += stringify(mdat_end - len(head)) + b"mdat"
    dstfile.seek(0)
    dstfile.write(head)
    remainder = BLOCKSIZE - len(head)

    if remainder >= 0:
        srcfile.seek(mdat.offset + 8)
        dstfile.write(srcfile.read(remainder))

    return 0


##### Main
def main():
    if not 3 <= len(sys.argv) <= 4 :
        print("\nUsage: {} <mp4_file> <container_file> [<hybrid_file>]".format(sys.argv[0]))
        print("\n\tEmbeds mp4 file <mp4_file> into VeraCrypt container <container_file>\n\
        and writes the result to <hybrid_file> if provided, else into 'output.mp4'.\n\
        <hybrid_file> can then be opened as a mp4 video file or as a VeraCrypt container.")
        return

    try:
        mp4file = open(sys.argv[1], mode="rb")
    except IOError as e:
        logger.error("Error while opening video file\n{}".format(e))
        sys.exit(1)

    try:
        outname = sys.argv[3] if len(sys.argv) == 4 else "output.mp4"
        outfile = open(outname, mode="wb")
    except IOError as e:
        logger.error("Error while opening output file\n{}".format(e))
        sys.exit(1)

    try:
        shutil.copyfile(sys.argv[2], outname)
    except IOError as e:
        logger.error("Could not copy volume into output file:\n{}".format(e))
        sys.exit(1)

    try:
        sys.exit(embed(mp4file, outfile))
    except RuntimeError as e:
        logger.error("Error: {}".format(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
