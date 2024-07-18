from database import retrieve_songs, add_songs, get_database_size, TrackInfo
from analysis import apply_pca, find_similarity, get_playlist_info
from local import print_data

## Based on a playlist, return a list of TrackInfos (track_id and distance). The list has `amount` items, the most similar ones, based on distance.
def find_songs(playlist: str, amount:int, adding:bool=False) -> list[TrackInfo]:
    data = get_playlist_info(playlist)
    analysis = data.analysis
    ids = data.ids
    songs = data.songs

    database = retrieve_songs(filters=f"WHERE track_id NOT IN {ids}")
    if adding or get_database_size() < 2000:
        add_songs(analysis, songs) ## Add playlist's songs to our database (slows down the process, but refines it)
    user_vector = apply_pca(analysis)

    return data.infos, find_similarity(user_vector, database, amount)

## Local search always add playlist's songs to our database
if __name__ == "__main__":
    playlist = input("Playlist: ")
    amount = int(input("Amount: "))
    infos, data = find_songs(playlist, amount, adding=True)
    print_data(data)