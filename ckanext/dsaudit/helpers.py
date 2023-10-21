from ckan import model
from ckan.plugins.toolkit import h, config

def dsaudit_resource_url(resource_id):
    package_id = model.Resource.get(resource_id).package_id
    pkg = model.Package.get(package_id)
    return h.url_for(
        pkg.type + '_resource.read',
        id=pkg.name,
        resource_id=resource_id,
    )

def dsaudit_data_columns(data):
    if data.get('records'):
        recs = data['records']
        if data.get('fields'):
            return [
                f['id'] for f in data['fields']
                if any(f['id'] in r for r in recs)
            ]
        seen = set()
        cols = []  # maintain order from dict keys
        for r in recs:
            unseen = set(r) - seen
            if unseen:
                cols += [k for k in r if k in unseen]
                seen.update(unseen)
        return cols
    return []

def dsaudit_preview_records():
    return int(config.get('ckanext.dsaudit.preview_records', 12))
