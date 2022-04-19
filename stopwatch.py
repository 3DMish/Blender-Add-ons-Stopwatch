# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Stopwatch",
    "category": "Interface",
    "author": "3DMish (Mish7913)",
    "version": (0, 1, 0),
    "blender": (3, 00, 0),
    "wiki_url": "",
    "location": "View3D > Tool Shelf > Misc Tab > Stopwatch",
    "tracker_url": "https://3dmish.blogspot.com/",
    "description": "Stopwatch",
    }

import bpy, bmesh, time, datetime
from bpy.props import *

status = False;

def get_time_seconds(): return int(time.time());

class Stopwatch(bpy.types.Panel):   
    bl_category     = "Misc"
    bl_label        = "Stopwatch"
    bl_space_type   = "VIEW_3D"
    bl_region_type  = "UI"

    def draw(self, context):
        lc_main = self.layout.column(align=True);
        lc_row = lc_main.row(align = True);
        lc_row.prop(bpy.context.scene, "stop_seconds");
        lc_row.prop(bpy.context.scene, "tmp_seconds");
        lc_row.enabled = False;
        lc_main.prop(bpy.context.scene, "stop_string");
        lc_row = lc_main.row(align = True);
        lc_row.operator(
            "stopwatch.button", 
            icon="SNAP_FACE" if (status) else "PLAY",
            text="Stop" if (status) else "Start",
        );
        lc_row.operator("stopwatch.clear", icon="X", text="");

class Stopwatch_Button(bpy.types.Operator):
    bl_idname   = 'stopwatch.button'
    bl_label    = 'Start/Stop'
    bl_description  = 'Start and Stop Stopwatch'

    def execute(self, context):
        global status
        if (status == True):
            status = False;
            
            now_time = int(get_time_seconds() - bpy.context.scene.stop_seconds);
            now_time += bpy.context.scene.tmp_seconds; bpy.context.scene.tmp_seconds = now_time;
            bpy.context.scene.stop_seconds = get_time_seconds();
            bpy.context.scene.stop_string = str(datetime.timedelta(seconds=now_time));
        else:
            status = True;
            
            bpy.context.scene.stop_seconds = get_time_seconds();
        return {'FINISHED'}

class Stopwatch_Clear(bpy.types.Operator):
    bl_idname   = 'stopwatch.clear'
    bl_label    = 'Clear'
    bl_description  = 'Clear Stopwatch'

    def execute(self, context):
        bpy.context.scene.tmp_seconds = 0;
        bpy.context.scene.stop_seconds = 0;
        bpy.context.scene.stop_string = "";
        return {'FINISHED'}

def initSceneProperties(X=0, Y=0, Z=0):
    bpy.types.Scene.stop_seconds = bpy.props.IntProperty(name = "", default = 0);
    bpy.types.Scene.tmp_seconds = bpy.props.IntProperty(name = "", default = 0);
    bpy.types.Scene.stop_string  = bpy.props.StringProperty(name="", description='Time');
    return
initSceneProperties();

def register():
    bpy.utils.register_class(Stopwatch);
    bpy.utils.register_class(Stopwatch_Button);
    bpy.utils.register_class(Stopwatch_Clear);

def unregister():
    bpy.utils.unregister_class(Stopwatch);
    bpy.utils.unregister_class(Stopwatch_Button);
    bpy.utils.unregister_class(Stopwatch_Clear);

if __name__ == "__main__":
    register()
