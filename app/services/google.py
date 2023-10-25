from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'

PERMISSIONS_BODY = {'type': 'user',
                    'role': 'writer',
                    'emailAddress': settings.email}

SPREADSHEET_BODY = {
    'properties': {'title': '',
                   'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист1',
                               'gridProperties': {'rowCount': 100,
                                                  'columnCount': 11}}}]
}

TABLE_VALUES = [
    ['Отчет от', '{now_date_time}'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    SPREADSHEET_BODY['properties']['title'] = 'Отчет на {}'.format(datetime.now().strftime(FORMAT))
    service = await wrapper_services.discover('sheets', 'v4')

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSIONS_BODY,
            fields="id"
        ))


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: list,
    wrapper_services: Aiogoogle
) -> None:
    TABLE_VALUES[0][1] = TABLE_VALUES[0][1].format(
        now_date_time=format(datetime.now().strftime(FORMAT))
    )
    service = await wrapper_services.discover('sheets', 'v4')

    for proj in projects:
        new_row = [str(proj['name']), str(proj['project_lifetime']), str(proj['description'])]
        TABLE_VALUES.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': TABLE_VALUES
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
