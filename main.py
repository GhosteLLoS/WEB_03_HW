import argparse
import logging
from pathlib import Path
from shutil import copyfile
from threading import Thread

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="Мотлох")

args = vars(parser.parse_args())

source = Path(args.get("source"))
output = Path(args.get("output"))

folders = []


def grab_folders(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grab_folders(el)


def copy_file(path: Path) -> None:
    for el in path.iterdir():
        ext = el.suffix[1:]
        new_folder = output / ext
        try:
            new_folder.mkdir(parents=True, exist_ok=True)
            copyfile(el, new_folder / el.name)
        except OSError as err:
            logging.error(err)



if __name__ == "__main__":

    logging.basicConfig(level=logging.ERROR, format="%(threadName)s %(message)s")
    grab_folders(source)
    folders.append(source)

    print(source, output)
    print(folders)

    threads = []
    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)
        
    [th.join() for th in threads]
    
    


