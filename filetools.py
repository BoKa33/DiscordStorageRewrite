import os, discord, asyncio, shutil, requests

#1.A #1.B.A
def split_file(file, chunk_size=7 * 1024 * 1024, outputdir="temp", step=""):
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

#1.B.B
def upload_temp_to_urllist(step=""):
    print(f"{step} Uploading...")
    links = []
    
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        channel = client.get_channel(<ADD CHANNEL HERE!!!!>)
        totalcount = len(os.listdir("temp"))
        for file in os.listdir("temp"):
            with open(f"temp/{file}", "rb") as f:
                message = await channel.send(file=discord.File(f,filename=f.name.split('/')[1]))
                links.append(message.attachments[0].url)
                print("\t",len(links), " from ", totalcount, end="\r")
        await client.close()
    
    client.run(<"ADD TOKEN HERE !!!!!">,log_handler=None)
    print()
    return links


#2.B.B
def download_urllist_to_temp(file_urls, step=""):
    print(f"{step} Downloading...")
    os.makedirs("temp", exist_ok=True)
    progress = 0
    for url in file_urls:
        progress += 1
        print("\t",progress," from ",len(file_urls),end="\r")
        response = requests.get(url.strip("\n"))
        filename = os.path.join("temp", url.split("/")[-1].strip("\n"))
        with open(filename, "wb") as f:
            f.write(response.content)
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

def clear_temp(log=0, temp_dir="temp"):
    if(log):
        print(f"\t0.X clear ", temp_dir)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

#Predefined routines:

#1:
def file_to_linkslistsfile_presplit(big_file):                                                  #1 (Upload)
    clear_temp(temp_dir="presplit")
    split_file(big_file, chunk_size = 350 * 1024 * 1024, outputdir="presplit", step="1.A")        #1.A
    urllists = []
    print("1.B:")                                                                                   #1.B:
    for big_file_chunk in os.listdir("presplit"):                                                   
        os.rename("presplit/"+big_file_chunk,big_file_chunk)                                            
        clear_temp()                                                                                    
        split_file(big_file_chunk,step="\t1.B.A")                                                         #1.B.A
        os.remove(big_file_chunk)                                                                       
        links = upload_temp_to_urllist(step="\t1.B.B")                                                    #1.B.B
        clear_temp()                                                                                    
        urllists.append(links);print("\t1.B.C")                                                           #1.B.C
    list_to_file(urllists,big_file,".linkslists",step="1.C")                                        #1.C         


#2:
def linkslistsfile_to_file_presplit(linkslistsfile):                                            #2  (Download)
    clear_temp();clear_temp(temp_dir="presplit")
    linkslists = file_to_list(linkslistsfile, ".linkslists",step="2.C")                             #2.C
    big_chunk_counter = 0
    '''print("big_chunks: ",len(linkslists))
    debug_counter = 0
    for linkslist in linkslists:
        print("\tLinklist: ", debug_counter, " Length: ", len(linkslist))
        debug_counter += 1'''
    big_chunk_counter = 0
    print("2.B:")                                                                                   #2.B:
    for linkslist in linkslists:                                                                    
        #print("downloading Linklist: ",big_chunk_counter)
        links = linkslist.strip().split(' ');print("\t2.B.C")                                             #2.B.C
        download_urllist_to_temp(links,step="\t2.B.B")                                                    #2.B.B
        big_chunk_file = linkslistsfile+"."+str(links[0].split(".")[-2]) # ->str(get big_chunk_id)                                   
        #print(big_chunk_file)                                                                       
        merge_file(big_chunk_file,step="\t2.B.A")                                                         #2.B.A
        os.rename(big_chunk_file, "presplit/"+big_chunk_file)
        big_chunk_counter += 1 
    merge_file(linkslistsfile, inputdir="presplit",step="2.A")                                      #2.A
    clear_temp();clear_temp(temp_dir="presplit")


"""
def file_to_linksfile(file, presplit=1):             #A          (Upload)
    clear_temp()                                #0.X
    split_file(file)                            #1.A
    links = upload_temp_to_urllist()            #1.B
    clear_temp()                                #X.0
    list_to_file(links,file,".links")        #1.C

def linksfile_to_file(linkfile, presplit=1):         #B          (Download)
    links = file_to_list(linkfile,".links")     #2.C
    clear_temp()                                #0.X
    download_urllist_to_temp(links)             #2.B
    merge_file(linkfile)                        #2.A
    clear_temp()                                #0.X
"""    


