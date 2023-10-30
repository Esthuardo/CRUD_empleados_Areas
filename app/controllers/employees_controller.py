from app.models.employee_model import EmployeeModel
from app.schemas.employees_schema import EmployeesResponseSchema
from app import db
from http import HTTPStatus


class EmployeesController:
    def __init__(self):
        self.db = db
        self.model = EmployeeModel
        self.schema = EmployeesResponseSchema

    def fetch_all(self, email=None, name=None):
        try:
            query = self.model.query.order_by("id")

            if email:
                query = query.filter(self.model.email == email)

            if name:
                query = query.filter(self.model.name == name)

            employees = query.paginate(page=1, per_page=10)

            response = self.schema(many=True)
            return {
                "resultados": response.dump(employees),
                "paginación": {
                    "totalEmpleados": employees.total,
                    "totalPáginas": employees.pages,
                    "porPágina": employees.per_page,
                    "páginaActual": employees.page,
                },
            }, HTTPStatus.OK
        except Exception as e:
            return {
                "mensaje": "Ocurrió un error",
                "error": str(e),
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def save(self, body):
        try:
            new_employee = self.model.create(**body)
            new_employee.hash_password()
            self.db.session.add(new_employee)
            self.db.session.commit()
            return {
                "message": f'El empleado {body["name"]} se creo exitosamente'
            }, HTTPStatus.CREATED
        except Exception as e:
            self.db.session.rollback()
            return {
                "message": "Ocurrio un error al guardar el empleado",
                "error": str(e),
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        finally:
            self.db.session.close()

    def update(self, id, new_body):
        try:
            employee_update = self.model.where(id=id).first()
            if employee_update:
                employee_update.update(**new_body)
                self.db.session.add(employee_update)
                self.db.session.commit()
                return {
                    "message": f"Se actualizo correctamente el empleado con id: {id}"
                }, HTTPStatus.OK
            else:
                return {
                    "message": f"No se encontro ningún empleado con el id {id}"
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
            employee_remove = self.model.where(id=id).first()
            if employee_remove:
                self.db.session.delete(employee_remove)
                self.db.session.commit()
                return {
                    "message": f"El empleado con el id {id} fue eliminada correctamente"
                }, HTTPStatus.OK
            else:
                return {
                    "message": f"No se encontro ningún empleado con el id {id}"
                }, HTTPStatus.NOT_FOUND
        except Exception as e:
            self.db.session.rollback()
            return {
                "message": "Ocurrio un error al eliminar",
                "error": str(e),
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        finally:
            self.db.session.close()

    def profile_me(self, identity):
        try:
            record = self.model.where(id=identity).first()
            response = self.schema(many=False)
            return response.dump(record), HTTPStatus.OK
        except Exception as e:
            self.db.session.rollback()
            return {
                "message": "Ocurrio un error",
                "error": str(e),
            }, HTTPStatus.INTERNAL_SERVER_ERROR
