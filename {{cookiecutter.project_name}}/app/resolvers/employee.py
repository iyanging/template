from typing import Optional

from gql import field_resolver, mutate, query
from gql.parser import parse_info

from app import types
from app.db import models, transaction


@field_resolver("Employee", "image")
async def employee_image(parent, info):
    loader = info.context["loaders"]["employee_image"]
    return await loader.load(int(parent.id))


@mutate
@transaction
async def create_employee(_, info, input: dict) -> types.Employee:
    obj_in = types.CreateEmployeeInput(**input)
    employee_id = await models.Employee.objects.create(obj_in)
    await models.EmployeeImage.objects.create_many(
        [dict(employee_id=employee_id, image_id=v) for v in obj_in.images]
    )
    return await get_an_employee(_, info, employee_id)


@query("employee")
async def get_an_employee(_, info, id: types.ID) -> Optional[types.Employee]:
    filter_obj = types.EmployeeFilterInput(id=id, is_deleted=False)
    return await models.Employee.objects.filter_by_model(filter_obj).load(parse_info(info)).first()
