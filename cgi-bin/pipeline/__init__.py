import glob
__all__ = [f.split("/")[1].split(".")[0] for f in glob.glob("pipeline/*.py")]
