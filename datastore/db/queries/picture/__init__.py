class PictureUploadError(Exception):
    pass


class PictureNotFoundError(Exception):
    pass


class PictureSetCreationError(Exception):
    pass


class PictureSetNotFoundError(Exception):
    pass


class PictureUpdateError(Exception):
    pass


"""
This module contains all the queries related to the Picture and PictureSet tables.
"""


def new_picture_set(cursor, picture_set, user_id: str):
    """
    This function uploads a new PictureSet to the database.

    Parameters:
    - cursor (cursor): The cursor of the database.
    - picture_set (str): The PictureSet to upload. Must be formatted as a json
    - user_id (str): The UUID of the user uploading.

    Returns:
    - The UUID of the picture_set.
    """
    try:
        query = """
            INSERT INTO 
                picture_set(
                    picture_set,
                    owner_id
                    )
            VALUES
                (%s,%s)
            RETURNING id    
            """
        cursor.execute(
            query,
            (
                picture_set,
                user_id,
            ),
        )
        return cursor.fetchone()[0]
    except Exception:
        raise PictureSetCreationError("Error: picture_set not uploaded")


def new_picture(cursor, picture, picture_set_id: str, seed_id: str, nb_objects=0 ):
    """
    This function uploads a NEW PICTURE to the database.

    Parameters:
    - cursor (cursor): The cursor of the database.
    - picture (str): The Picture METADATA to upload. Must be formatted as a json
    - picture_set_id (str): The UUID of the Picture_set the picture is in.
    - seedID (str): The UUID of the seed the picture is linked to.
    - nb_objects (int): The number of objects in the picture.

    Returns:
    - The UUID of the picture.
    """
    try:
        query = """
            INSERT INTO 
                picture(
                    picture,
                    picture_set_id,
                    nb_obj
                    )
            VALUES
                (%s,%s,%s)
            RETURNING id
                """
        cursor.execute(
            query,
            (
                picture,
                picture_set_id,
                nb_objects,
            ),
        )
        picture_id = cursor.fetchone()[0]
        query = """
            INSERT INTO 
                picture_seed(
                    seed_id,
                    picture_id
                    )
            VALUES
                (%s,%s)
                """
        cursor.execute(
            query,
            (
                seed_id,
                picture_id,
            ),
        )
        return picture_id
    except Exception:
        raise PictureUploadError("Error: Picture not uploaded")

def new_picture_unknown(cursor, picture, picture_set_id:str, nb_objects=0):
    """
    This function uploads a NEW PICTURE to the database.

    Parameters:
    - cursor (cursor): The cursor of the database.
    - picture (str): The Picture METADATA to upload. Must be formatted as a json
    - picture_set_id (str): The UUID of the Picture_set the picture is in.
    - nb_objects (int): The number of objects in the picture.

    Returns:
    - The UUID of the picture.
    """
    try:
        query = """
            INSERT INTO 
                picture(
                    picture,
                    picture_set_id,
                    nb_obj
                    )
            VALUES
                (%s,%s,%s)
            RETURNING id
                """
        cursor.execute(
            query,
            (
                picture,
                picture_set_id,
                nb_objects,
            ),
        )
        return cursor.fetchone()[0]
    except Exception:
        raise PictureUploadError("Error: Picture not uploaded")


def get_picture_set(cursor, picture_set_id: str):
    """
    This function retrieves a PictureSet from the database.

    Parameters:
    - cursor (cursor): The cursor of the database.
    - picture_set_id (str): The UUID of the PictureSet to retrieve.

    Returns:
    - The PictureSet in json format.
    """
    try:
        query = """
            SELECT
                picture_set
            FROM
                picture_set
            WHERE
                id = %s
                """
        cursor.execute(query, (picture_set_id,))
        return cursor.fetchone()[0]
    except Exception:
        raise PictureSetNotFoundError(f"Error: PictureSet not found:{picture_set_id}")


def get_picture(cursor, picture_id: str):
    """
    This function retrieves a Picture from the database.

    Parameters:
    - cursor (cursor): The cursor of the database.
    - picture_id (str): The UUID of the Picture to retrieve.

    Returns:
    - The Picture in json format.
    """
    try:
        query = """
            SELECT
                picture
            FROM
                picture
            WHERE
                id = %s
                """
        cursor.execute(query, (picture_id,))
        return cursor.fetchone()[0]
    except Exception:
        raise PictureNotFoundError(f"Error: Picture not found: {picture_id}")


def get_user_latest_picture_set(cursor, user_id: str):
    """
    This function retrieves the latest picture_set of a specific user from the database.

    Parameters:
    - cursor (cursor): The cursor of the database.
    - user_id (str): The UUID of the user to retrieve the picture_set from (the owner).

    Returns:
    - The picture_set in json format.
    """
    try:
        query = """
            SELECT
                picture_set
            FROM
                picture_set
            WHERE
                owner_id = %s
            ORDER BY
                upload_date
            DESC
            LIMIT 1
                """
        cursor.execute(query, (user_id,))
        return cursor.fetchone()[0]
    except Exception:
        raise PictureSetNotFoundError(
            f"Error: picture_set not found for user:{user_id} "
        )


def update_picture_metadata(cursor, picture_id: str, metadata: dict, nb_objects: int):
    """
    This function updates the metadata of a picture in the database.

    Parameters:
    - cursor (cursor): The cursor of the database.
    - picture_id (str): The UUID of the picture to update.
    - metadata (dict): The metadata to update. Must be formatted as a json.

    Returns:
    - None
    """
    try:
        query = """
            UPDATE
                picture
            SET
                picture = %s,
                nb_obj = %s
            WHERE
                id = %s
            """
        cursor.execute(query, (metadata,nb_objects, picture_id))
    except Exception:
        raise PictureUpdateError(f"Error: Picture metadata not updated:{picture_id}")


def is_a_picture_set_id(cursor, picture_set_id):
    """
    This function checks if a picture_set_id exists in the database.

    Parameters:
    - cursor (cursor): The cursor of the database.
    - picture_set_id (str): The UUID of the picture_set to check.
    """
    try:
        query = """
            SELECT EXISTS(
                SELECT 
                    1 
                FROM 
                    picture_set
                WHERE 
                    id = %s
            )
                """
        cursor.execute(query, (picture_set_id,))
        res = cursor.fetchone()[0]
        return res
    except Exception:
        raise Exception("unhandled error")
