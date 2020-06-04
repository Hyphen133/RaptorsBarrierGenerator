import uuid


class SessionPolygonManagement:
    def __init__(self) -> None:
        super().__init__()
        self.session_polygons_map = {}

    def delete_polygon(self, session_token, id):
        self.session_polygons_map[session_token] = [id_polygon for id_polygon in self.session_polygons_map[session_token] if id_polygon.get_id() != id]

    def add_polygons_for_session(self, session_token, polygons):
        self.session_polygons_map[session_token] = polygons


class IdentifiablePolygon:
    def __init__(self, polygon):
        self.id = uuid.uuid1()
        self.polygon = polygon

    def get_id(self):
        return self.id

    def get_polygon(self):
        return self.polygon