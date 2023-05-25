import os
import sys
import math
import numpy
import generate_mesh_size_function

sys.path.append( "/opt/Coreform-Cubit-2023.4/bin" )
import cubit

def main( geom_params ):
    build_indenter( geom_params )
    build_target( geom_params )
    build_assembly()

def build_indenter( geom_params ):
    cubit.cmd( "reset" )
    tip_radius = geom_params[ "tip_radius" ]
    shaft_radius = geom_params[ "shaft_radius" ]
    shaft_standoff = geom_params[ "shaft_standoff" ]
    wedge_angle = numpy.deg2rad( geom_params[ "wedge_angle" ] )

    x = numpy.zeros( 6 )
    y = numpy.zeros( 6 )

    # Known values
    x[0] = 0.0
    x[1] = 0.0
    x[3] = shaft_radius
    x[4] = shaft_radius
    x[5] = 0.0
    y[0] = 0.0
    y[1] = tip_radius

    # Compute driven values
    x[2] = tip_radius * math.cos( wedge_angle )
    y[2] = y[0] + ( tip_radius - ( tip_radius * math.sin( wedge_angle ) ) )
    y[3] = y[2] + ( shaft_radius - x[2] ) / math.tan( wedge_angle )
    y[4] = y[3] + shaft_standoff
    y[5] = y[4]

    for i in range( 0, len( x ) ):
        cubit.cmd( f"create vertex {x[i]} {y[i]}" )

    cubit.cmd( "create curve arc center vertex 2 1 3" )
    cubit.cmd( "create curve vertex 3 4" )
    cubit.cmd( "create curve vertex 4 5" )
    cubit.cmd( "create curve vertex 5 6" )
    cubit.cmd( "create curve vertex 6 1" )
    cubit.cmd( "create surface curve all" )

    cubit.cmd( "sideset 1 curve 4" )
    cubit.cmd( "sideset 2 curve 3" )
    cubit.cmd( "sideset 3 curve 2" )
    cubit.cmd( "sideset 4 curve 1" )
    cubit.cmd( "sideset 5 curve 5" )
    cubit.cmd( "sideset 100 curve all" )
    cubit.cmd( "sideset 1 name 'indenter_top'")
    cubit.cmd( "sideset 2 name 'indenter_standoff'")
    cubit.cmd( "sideset 3 name 'indenter_wedge'")
    cubit.cmd( "sideset 4 name 'indenter_tip'")
    cubit.cmd( "sideset 5 name 'indenter_axis'")
    cubit.cmd( "sideset 100 name 'indenter_boundaries'")
    cubit.cmd( "nodeset 10 vertex 1" )
    cubit.cmd( "nodeset 10 name 'indenter_tip_node'")

    cubit.cmd( "delete vertex all" )
    cubit.cmd( "compress" )

    cubit.cmd( "surface 1 rename 'indenter'" )
    cubit.cmd( "surface indenter scheme pave" )
    cubit.cmd( "surface indenter size 0.25" )
    cubit.cmd( "mesh surface indenter" )
    cubit.cmd( "block 1 surface indenter" )
    cubit.cmd( "block 1 element type QUAD" )
    cubit.cmd( "block 1 name 'indenter'" )
    cubit.cmd( "save cub5 'indenter.cub5' overwrite")
    cubit.cmd( "export mesh 'indenter.e' overwrite")
    generate_mesh_size_function.doIndenter( geom_params )
    cubit.cmd( "delete mesh" )
    cubit.cmd( "import sizing function 'indenter_mesh.e' block 1 variable 'meshSize' time 0.0" )
    cubit.cmd( "surface 1 sizing function exodus min_size 0.25 max_size 5.0" )
    cubit.cmd( "mesh surface indenter" )
    cubit.cmd( "save cub5 'indenter.cub5' overwrite")
    cubit.cmd( "export mesh 'indenter.e' overwrite")
    cubit.cmd( "reset" )

def build_target( geom_params ):
    target_width = geom_params[ "target_width" ]
    target_height = geom_params[ "target_height" ]
    cubit.cmd( "reset" )
    cubit.cmd( f"create surface rectangle width {target_width} height {target_height} zplane" )
    cubit.cmd( f"move surface 1 x {target_width / 2.0} y {-1.0 * target_width / 2.0}" )

    cubit.cmd( "sideset 6 curve 1" )
    cubit.cmd( "sideset 7 curve 2" )
    cubit.cmd( "sideset 8 curve 3" )
    cubit.cmd( "sideset 9 curve 4" )
    cubit.cmd( "sideset 200 curve 1 2 3 4" )
    cubit.cmd( "nodeset 20 vertex 2" )

    cubit.cmd( "sideset 6 name 'target_top'" )
    cubit.cmd( "sideset 7 name 'target_right'" )
    cubit.cmd( "sideset 8 name 'target_bot'" )
    cubit.cmd( "sideset 9 name 'target_left'" )
    cubit.cmd( "sideset 200 name 'target_boundaries'" )
    cubit.cmd( "nodeset 20 name 'target_depth_node'")

    cubit.cmd( "surface 1 scheme pave" )
    cubit.cmd( "surface 1 size 0.25" )
    cubit.cmd( "mesh surface 1" )
    cubit.cmd( "block 2 surface 1" )
    cubit.cmd( "block 2 element type QUAD" )
    cubit.cmd( "block 2 name 'material_target'" )
    cubit.cmd( "save cub5 'target.cub5' overwrite")
    cubit.cmd( "export mesh 'target.e' overwrite")
    generate_mesh_size_function.doTarget( geom_params )
    cubit.cmd( "delete mesh" )
    cubit.cmd( "import sizing function 'target_mesh.e' block 2 variable 'meshSize' time 0.0" )
    cubit.cmd( "surface 1 sizing function exodus min_size 0.25 max_size 5.0" )
    cubit.cmd( "mesh surface 1" )
    cubit.cmd( "save cub5 'target.cub5' overwrite")
    cubit.cmd( "export mesh 'target.e' overwrite")
    cubit.cmd( "reset" )

def build_assembly( ):
    cubit.cmd( "reset" )
    cubit.cmd( "import mesh geometry 'indenter.e' feature_angle 135.00  merge" )
    cubit.cmd( "import mesh geometry 'target.e' feature_angle 135.00  merge" )
    cubit.cmd( "compress" )
    cubit.cmd( "export mesh 'nano_indenter_rz.e' overwrite" )
    cubit.cmd( "reset" )

if __name__ == "__main__":
    geom_params = { "tip_radius": 10, "shaft_radius": 25, "shaft_standoff": 10, "wedge_angle": numpy.deg2rad( 20 ) }
    geom_params['target_width'] = 1.5 * geom_params['shaft_radius']
    geom_params['target_height'] = geom_params['target_width']
    target_width = geom_params[ "target_width" ]
    target_height = geom_params[ "target_height" ]
    main( geom_params )