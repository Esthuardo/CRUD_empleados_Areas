from app.models.area_model import AreaModel
from app.schemas.areas_schema import AreaResponseSchema
from app import db
from http import HTTPStatus


class AreaController:
    def __init__(self):
        self.db = db
        self.model = AreaModel
        self.schema = AreaResponseSchema

    def fetch_all(self):
        areas = self.model.all()
        response = self.schema(many=True)
        return response.dump(areas), HTTPStatus.OK

    def save(self, body):
        try:
            new_area = self.model.create(**body)
            self.db.session.add(new_area)
            self.db.session.commit()
            return {
                "message": f'El área {body["name"]} se creo exitosamente'
            }, HTTPStatus.CREATED
        except Exception as e:
            self.db.session.rollback()
            return {
                "message": "Ocurrio un error al guardar el área",
                "error": str(e),
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        finally:
            self.db.session.close()

    def find_by_id(self, find_id):
        try:
            areas = self.model.where(id=find_id).first()
            if areas:
                response = self.schema()
                return response.dump(areas), HTTPStatus.OK
            else:
                return {
                    "message": f"No se encontro ningún área con el id {find_id}"
                }, HTTPStatus.NOT_FOUND
        except Exception as e:
            return {
                "message": "Ocurrio un error al buscar el área",
                "error": str(e),
            }, HTTPStatus.NOT_FOUND

    def update(self, id, new_body):
        try:
            area_update = self.model.where(id=id).first()
            if area_update:
                area_update.update(**new_body, commit=False)
                self.db.session.add(area_update)
                self.db.session.commit()
                return {
                    "message": f"Se actualizo correctamente el área con id: {id}"
                }, HTTPStatus.OK
            else:
                return {
                    "message": f"No se encontro ningún área con el id {id}"
                }, HTTPStatus.NOT_FOUND
        except Exception as e:
            self.db.session.rollback()
            return {
                "message": "Ocurrio un error al actualizar",
                "error": str(e),
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        finally:
            self.db.session.close()

    def remove(self, id):
        try:
            area_remove = self.model.where(id=id).first()
            if area_remove:
                self.db.session.delete(area_remove)
                self.db.session.commit()
                return {
                    "message": f"El área con el id {id} fue eliminada correctamente"
                }, HTTPStatus.OK
            else:
                return {
                    "message": f"No se encontro ningún área con el id {id}"
                }, HTTPStatus.NOT_FOUND
        except Exception as e:
            self.db.session.rollback()
            return {
                "message": "Ocurrio un error al eliminar",
                "error": str(e),
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        finally:
            self.db.session.close()
