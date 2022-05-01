from email.mime import audio
from operator import truediv
from tkinter import filedialog
from tkinter import *
import mutagen
from mutagen.id3 import ID3, TIT2
import pathlib as pl
import os


def collect_all_media_files(folder_selected):
    all_books = []
    for file in pl.Path(folder_selected).glob('**/*'):
        if ".mp3" in str(file) or ".m4b" in str(file) or ".m4a" in str(file):
            if not check_filepath_in_dict(all_books, str(file.parent)):
                all_books.append( {"name": file.parts[-2] ,"directory" : str(file.parent), "files" : [str(file)], "metadata_file" : f'{str(file.parent)}\metadata.abs' })
            else:
                for directory in all_books:
                    if str(file.parent) == directory.get("directory"):
                        directory.get("files").append(str(file))
                        break
    return media_files_with_metadata(all_books)


def check_filepath_in_dict(all_books, current_parent_dir):
    for all_files in all_books:
        if all_files.get("directory") == current_parent_dir:
            return True
    return False

def media_files_with_metadata(all_books):
    books_with_metadata = []
    for book in all_books:
        if os.path.isfile(book.get("metadata_file")):
            books_with_metadata.append(book)
        else:
            print(f'{book.get("name")} DOES NOT HAVE A METADATA FILE')
    return books_with_metadata

def parse_abs_metadata_to_id3(all_books):
    for book in all_books:
        with open(book.get("metadata_file"), 'rt', encoding='utf-8') as metadata_info:
            id3_tags = {}
            lines = metadata_info.readlines()
            counter = 0
            for line in lines:
                if counter >= 1:
                    id3_tags["Description"] = line
                    counter = 0
                line = line.strip('\n').split('=')
                if len(line) > 1:
                    if "authors" in line[0]:
                        if line[1] != None or line[1] != '':
                            id3_tags["Artist"] = line[1]
                    elif "publisher" in line[0]:
                        if line[1] != None or line[1] != '':
                            id3_tags["Album Artist"] = line[1]
                    elif "narrators" in line[0]:
                        if line[1] != None or line[1] != '':
                            id3_tags["Narrator"] = line[1]
                    elif "title" in line[0]:
                        if line[1] != None or line[1] != '':
                            if 'subtitle' not in line[0]:
                                id3_tags["Album"] = line[1]
                    elif "series" in line[0]:
                        if line[1] != None or line[1] != '':
                            id3_tags["Album Sort Name"] = line[1]
                    elif "publishedYear" in line[0]:
                        if line[1] != None or line[1] != '':
                            id3_tags["Published Year"] = line[1]
                
                if "[DESCRIPTION]" in line[0]:
                    counter+=1
                elif "[CHAPTER]" in line[0]:
                    break
        book['ID3_tags'] = id3_tags
    return all_books


root = Tk()
root.withdraw()
folder_selected = '\\\\TOWER\\Media\\Audio\\Audiobooks\\Unsorted Audiobooks\\Tag Testing\\Alec Hutson'
#folder_selected = '\\\\TOWER\\Media\\Audio\\Audiobooks\\Unsorted Audiobooks\\Beeg jobs\\Robin Hobb'
#folder_selected = filedialog.askdirectory()

all_books = collect_all_media_files(folder_selected)
all_books = parse_abs_metadata_to_id3(all_books)

for book in all_books:
    for file in book.get("files"):
        audio_file = mutagen.File(file, easy=True)
        non_easy_audio_file = mutagen.File(file)

        print("==================================================================")
        print(audio_file.tags.pprint())
        print("==================================================================")
        print(non_easy_audio_file.tags.pprint())         
        non_easy_audio_file["©alb"] = f'{book.get("ID3_tags").get("Album")}'
        non_easy_audio_file["©ART"] = f'{book.get("ID3_tags").get("Artist")}'
        non_easy_audio_file["aART"] = f'{book.get("ID3_tags").get("Album Artist")}'
        non_easy_audio_file["©day"] = f'{book.get("ID3_tags").get("Album Sort Name")}'
        non_easy_audio_file["date"] = f'{book.get("ID3_tags").get("Published Year")}'
        non_easy_audio_file["©cmt"] = f'{book.get("ID3_tags").get("Description")}'
        non_easy_audio_file["©nrt"] = f'{book.get("ID3_tags").get("Narrator")}'

        non_easy_audio_file.save()
        print("==================================================================")
        print(non_easy_audio_file.tags.pprint())  
        print("==================================================================")
        '''
        audio_file = mutagen.File(file, easy=True)
        audio_file["album"] = f'{book.get("ID3_tags").get("Album")}'
        audio_file["artist"] = f'{book.get("ID3_tags").get("Artist")}'
        audio_file["albumartist"] = f'{book.get("ID3_tags").get("Album Artist")}'
        audio_file["albumsort"] = f'{book.get("ID3_tags").get("Album Sort Name")}'
        audio_file["date"] = f'{book.get("ID3_tags").get("Published Year")}'
        audio_file["comment"] = f'{book.get("ID3_tags").get("Description")}'
        #audio_file["composer"] = f'{book.get("ID3_tags").get("Narrator")}'
        #print(audio_file)
        audio_file.save()
        '''


print("Done!")

