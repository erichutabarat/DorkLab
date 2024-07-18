from lib.lab import Lab

def main():
    banner = r"""
    ______           _      _           _     
    |  _  \         | |    | |         | |    
    | | | |___  _ __| | __ | |     __ _| |__  
    | | | / _ \| '__| |/ / | |    / _` | '_ \ 
    | |/ / (_) | |  |   <  | |___| (_| | |_) |
    |___/ \___/|_|  |_|\_\ \_____/\__,_|_.__/ 
                                            
    """
    github = " Visit: https://github.com/erichutabarat/DorkLab\n\n"
    print(banner)
    print(github)
    keyword = input("Enter keyword: ")
    main_lab = Lab(keyword)
    
    main_lab.start()
    main_lab.close()

if __name__ == "__main__":
    main()