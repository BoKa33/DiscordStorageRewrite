import os, asyncio, shutil, requests, time;from telegram import Bot;from telegram.ext import Updater;from telegram.ext import CallbackContext

token = ADD TOKEN HERE
chat_id = ADD CHAT ID HERE
bot = Bot(token=token)

#1.A #1.B.A
def split_file(file, chunk_size= 20 * 1024 * 1024, outputdir="temp", step=""):
    print(f"{step} Splitting...")
    # Get the file size in bytes
    file_size = os.path.getsize(file)

    # Open the original file for reading
    with open(file, 'rb') as f:
        # Calculate the number of chunks
        num_chunks = file_size // chunk_size
        if file_size % chunk_size != 0:
            num_chunks += 1

        # Split the file into chunks
        for i in range(num_chunks):
            print("\t",i+1," from ",num_chunks,end="\r")
            chunk = f.read(chunk_size)
            chunk_file = f"{outputdir}/{file}.{i}"
            with open(chunk_file, 'wb') as chunk_f:
                chunk_f.write(chunk)
    print()
#2.A #2.B.A
def merge_file(file, inputdir="temp", step=""):
    print(f"{step} Merging...")
    # Get the original file name
    original_file = file

    # Open the original file for writing
    with open(original_file, 'wb') as f:
        i = 0
        while True:
            chunk_file = f"{inputdir}/{file}.{i}"
            print("\tmerged:",i,end="\r")
            if not os.path.exists(chunk_file):
                break
            with open(chunk_file, 'rb') as chunk_f:
                chunk = chunk_f.read()
                f.write(chunk)
            i += 1
    print()
#1.C
def list_to_file(given_list, filepath, ending, step=""):
    print(f"{step} Writing List...")
    with open(filepath+ending, "w") as f:
        progress = 0
        for line in given_list:
            progress += 1
            print("\t",progress," from ",len(given_list),end="\r")
            f.write(' '.join(line)+"\n")
    print()
#2.C
def file_to_list(filepath, ending, step=""):
    print(f"{step} Reading File...")
    with open(filepath+ending, "r") as f:
        lines = f.readlines()
        print("\tlines: ",len(lines))
        return lines
#0.X
def clear_temp(log=0, temp_dir="temp"):
    if(log):
        print(f"\t0.X clear ", temp_dir)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)


# ----------------------------

#1.B.B
def upload_temp_to_TIDlist(step=""):
    print(f"{step} Uploading...")

    temp_dir =  "temp"
    documentIDs = []

    async def main():
        pieces = len(os.listdir(temp_dir))
        counter = 0
        for file in os.listdir(temp_dir):
            counter += 1
            print("uploading: ", counter, " / ", pieces)
            documentID = await bot.send_document(chat_id, f"{temp_dir}/{file}")
            documentIDs.append(f"{file}|{documentID.document.file_id}")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    return documentIDs

#2.B.B
def download_TIDlist_to_temp(file_Identifiers, step=""):  # file_Identifiers is a List of "filename|fileID"
    print(f"{step} Downloading...")

    temp_dir =  "temp"
    os.makedirs(temp_dir, exist_ok=True)

    async def main():
        pieces = len(file_Identifiers)
        counter = 0
        for id in file_Identifiers:
            counter += 1
            print("downloading: ", counter, " / ", pieces)
            file_data = await bot.get_file(id.split("|")[1])
            file_content = requests.get(file_data.file_path).content
            filename = os.path.join("temp", id.split("|")[0])
            with open(filename, "wb") as f:
                f.write(file_content)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

# ----------------------------

#1:
def file_to_linkslistsfile_presplit(big_file):                                                  #1 (Upload)
    clear_temp(temp_dir="presplit")
    split_file(big_file, chunk_size = 1024 * 1024 * 1024, outputdir="presplit", step="1.A")    #1.A
    idlists = []
    print("1.B:")                                                                              #1.B:
    for big_file_chunk in os.listdir("presplit"):
        os.rename("presplit/"+big_file_chunk,big_file_chunk)
        clear_temp()
        split_file(big_file_chunk,step="\t1.B.A")                                                         #1.B.A
        os.remove(big_file_chunk)
        documentIDs = upload_temp_to_TIDlist(step="\t1.B.B")                                                    #1.B.B
        clear_temp()
        idlists.append(documentIDs);                                                           #1.B.C
    list_to_file(idlists,big_file,".tidlists",step="1.C")                                        #1.C


#2:
def linkslistsfile_to_file_presplit(idlistsfile):                                            #2  (Download)
    clear_temp();clear_temp(temp_dir="presplit")
    idlists = file_to_list(idlistsfile, ".tidlists",step="2.C")                             #2.C
    big_chunk_counter = 0
    print("2.B:")                                                                                   #2.B:
    for idlist in idlists:
        #print("downloading IDlist: ",big_chunk_counter)
        ids = idlist.strip().split(' ');                                             #2.B.C
        download_TIDlist_to_temp(ids,step="\t2.B.B")                                                    #2.B.B
        big_chunk_file = idlistsfile+"."+str(ids[0].split(".")[-2]) # ->str(get big_chunk_id)
        #print(big_chunk_file)
        merge_file(big_chunk_file,step="\t2.B.A")                                                         #2.B.A
        os.rename(big_chunk_file, "presplit/"+big_chunk_file)
        big_chunk_counter += 1
    merge_file(idlistsfile, inputdir="presplit",step="2.A")                                      #2.A
    clear_temp();clear_temp(temp_dir="presplit")

# Interface:

def uploadFile(file): #1
    file_to_linkslistsfile_presplit(file)

def downloadFile(linkfile): #2
    linkslistsfile_to_file_presplit(linkfile)

"""
def file_to_linksfile(file, presplit=1):             #1          (Upload)
    clear_temp()                                #0.X
    split_file(file)                            #1.A
    links = upload_temp_to_urllist()            #1.B
    clear_temp()                                #0.X
    list_to_file(links,file,".links")           #1.C

def linksfile_to_file(linkfile, presplit=1):         #2          (Download)
    links = file_to_list(linkfile,".links")     #2.C
    clear_temp()                                #0.X
    download_urllist_to_temp(links)             #2.B
    merge_file(linkfile)                        #2.A
    clear_temp()                                #0.X
"""
