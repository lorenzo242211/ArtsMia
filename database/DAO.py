from database.DB_connect import DBConnect
from model.oggetto import Oggetto
class DAO():

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM objects"""
        cursor.execute(query)

        for row in cursor:
            result.append(Oggetto(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesPesati():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT eo1.object_id as o1, eo2.object_id as o2, count(*) as pesoneee
                from exhibition_objects eo1, exhibition_objects eo2
                WHERE eo1.object_id < eo2.object_id and eo1.exhibition_id = eo2.exhibition_id 
                group by eo1.object_id, eo2.object_id
                 order by pesoneee desc"""
        cursor.execute(query)

        for row in cursor:
            result.append((row["o1"], row["o2"], row["pesoneee"])) #tupla di valori U, V e peso
        cursor.close()
        conn.close()
        return result
