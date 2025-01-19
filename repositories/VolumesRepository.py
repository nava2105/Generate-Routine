class VolumesRepository:
    def __init__(self, db_connection):
        self.connection = db_connection

    def get_volume_by_muscle_name(self, muscle_name: str):
        """
        Retrieves volume information for the specified muscle group.
        :param muscle_name: The name of the muscle group (e.g., 'quads', 'chest').
        :return: A dictionary containing volume data for the muscle group.
        """
        query = """
            SELECT * 
            FROM ptrainer_volumes.training_volumes
            WHERE muscle_group = %s;
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (muscle_name,))
                result = cursor.fetchone()
                if result:
                    return {
                        "muscle_group": result[0],
                        "mv": result[1],
                        "mev": result[2],
                        "mav": result[3],
                        "mrv": result[4],
                        "frequency_per_week": result[5],
                        "reps": result[6],
                        "rir": result[7],
                    }
                return None
        except Exception as e:
            print(f"Error fetching volume data: {e}")
            return None
