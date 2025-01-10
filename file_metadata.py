import re

string = "/media/kali/256/series/shogun/Shogun.[2024].S01E08.The.Abyss.of.Life.1080p.DSNP.WEB-DL.DDP5.1.H.264-FLUX.mkv"
def extract_info(file_name):
    # Extract file name without path
    title = file_name.split('/')[-1]
    title_splits = title.split(".")

    # Get extension
    extension = title_splits[-1]
    title_splits.remove(extension)

    # Extract the year from the filename (word boundary, square brackets, or parentheses)
    year_match = re.search(r'\b(19|20)\d{2}\b|\[(19|20)\d{2}]|\((19|20)\d{2}\)', title)
    year = year_match.group(0) if year_match else None

    # Extract the resolution from the filename
    resolution_match = re.search(r'\b(\d{3,4}p)\b|\[(\d{3,4}p)]|\((\d{3,4}p)\)', title)
    resolution = resolution_match.group(1) or resolution_match.group(2) or resolution_match.group(3) if resolution_match else None


    unnecessary_words = [
        "BluRay","x264","YIFY","DSNP", "WEB-DL", "DDP5","264-FLUX",
        "1", "H", "x264-[YTS", "x264-[YTS AG]", "REPACK", "AAC5", "1-[YTS",
        "YTS", "x265-ELiTE", "BrRip", "MX]", "AM]", "AG]", "LT]", "WEBRip",
        "x265", "10bit", "HEVC", "x265-MeGusta[EZTVx", "to]", "h264-ETHEL[EZTVx",
        "h264-successfulcrab[EZTVx", "BOKUTOX", "HEVC", "x265-MeGusta", "x264-tbs[eztv]",
        "webrip", "AAC-[YTS", "UNRATED", "Bluray",
        ]

    seen = {*""}
    try:
        title_splits.remove(year) if year else None
        title_splits.remove(resolution)
        title_splits = [
            word for word in title_splits 
            if word not in unnecessary_words 
            and not (word in seen or seen.add(word))
        ]
    except ValueError:
        pass

    title = " ".join(title_splits)

    return {
        'title': title,
        'year': year.strip('[]()') if year else "N/A",
        'extension': extension,
        'resolution': resolution.strip('[]()') if resolution else "N/A",
    }
