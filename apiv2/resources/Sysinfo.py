import uuid
from flask_restx import Namespace, Resource, fields
from .security import sec_admin, sec_contractor
from apiv2.models.Sysinfo import SystemInfo


apiSysinfoNamespace = Namespace('SysInfo', description="Information about the server.")

sysinfo_schema = apiSysinfoNamespace.model(name='SysInfo', model={
    'cpu_load': fields.Float(readonly=True,
                             description="CPU load in percent over the last 5 minutes.",
                             example=0.32),
    'ram_usage': fields.Float(readonly=True,
                              description="Current RAM usage in percent.",
                              example=0.62),
    'disk_usage': fields.Float(readonly=True,
                               description="Current disk usage in percent.",
                               example=0.33),
    'boot_time': fields.DateTime(readonly=True,
                                 description="Time, at which the server booted up."),
    'platform': fields.String(readonly=True,
                              description="OS platform string."),
})


@apiSysinfoNamespace.response(403, "You do not have access to this resource. "
                                   "The authorization you provided is not sufficient.")
@apiSysinfoNamespace.response(401, "Authorization required. You did not provide any valid authentication.")
@apiSysinfoNamespace.doc(security=['apikey'])
@apiSysinfoNamespace.route("/", endpoint='sysinfo')
class ExistingUserResource(Resource):
    @sec_contractor
    @apiSysinfoNamespace.doc(descpription="Get sysinfo")
    @apiSysinfoNamespace.marshal_with(sysinfo_schema, description="Current sysinfo")
    def get(self):
        return SystemInfo()