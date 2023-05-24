import os
import sys
import math
import numpy

sys.path.append( "/home/greg/apps/seacas/lib" )
import exodus

def doIndenter( geom_params ):
    base = exodus.exodus( "/home/greg/projects/cubit_dakota/indenter/indenter.e", array_type='numpy', mode="r" )
    E = base.copy( "/home/greg/projects/cubit_dakota/indenter/indenter_mesh.e", mode="a" )
    base.close()
    E.close()
    E = exodus.exodus( "/home/greg/projects/cubit_dakota/indenter/indenter_mesh.e", array_type='numpy', mode="a" )

    numNodes = E.num_nodes()
    nCoords = numpy.array( E.get_coords() )
    meshSize = numpy.zeros( numNodes )
    nodesInContactSideset = numpy.unique( E.get_side_set_node_list( 4 )[1] )
    maxY = max( nCoords[1] )
    contactMaxY = -float( "inf" )
    for i in range( 0, len( nodesInContactSideset ) ):
        node_idx = nodesInContactSideset[i]
        y = nCoords[1, node_idx-1]
        if y > contactMaxY:
            contactMaxY = y

    for i in range( 0, numNodes ):
        if nCoords[1,i] > contactMaxY:
            meshSize[i] = ( nCoords[1,i] - contactMaxY ) / ( maxY - contactMaxY )

    E.put_time( 1, 0.0 )
    exodus.add_variables( E, nodal_vars = ["meshSize"] )
    E.put_node_variable_values( "meshSize", 1, meshSize )
    E.close()

def doTarget( geom_params ):
    tipRadius = geom_params[ 'tip_radius' ]

    base = exodus.exodus( "/home/greg/projects/cubit_dakota/indenter/target.e", array_type='numpy', mode="r" )
    E = base.copy( "/home/greg/projects/cubit_dakota/indenter/target_mesh.e", mode="a" )
    base.close()
    E.close()
    E = exodus.exodus( "/home/greg/projects/cubit_dakota/indenter/target_mesh.e", array_type='numpy', mode="a" )

    numNodes = E.num_nodes()
    nCoords = numpy.array( E.get_coords() )
    meshSize = numpy.zeros( numNodes )
    dist = numpy.hypot( nCoords[0], nCoords[1] )
    maxDist = max( dist )

    for i in range( 0, len( nCoords[0] ) ):
        if dist[i] > tipRadius:
            meshSize[i] = ( dist[i] - tipRadius ) / ( maxDist - tipRadius )
    
    E.put_time( 1, 0.0 )
    exodus.add_variables( E, nodal_vars = ["meshSize"] )
    E.put_node_variable_values( "meshSize", 1, meshSize )
    E.close()

if __name__ == "__main__":
    geom_params = { "tip_radius": 10, "shaft_radius": 25, "shaft_standoff": 10, "wedge_angle": numpy.deg2rad( 20 ) }
    geom_params['target_width'] = 1.5 * geom_params['shaft_radius']
    geom_params['target_height'] = geom_params['target_width']
    target_width = geom_params[ "target_width" ]
    target_height = geom_params[ "target_height" ]
    doIndenter( geom_params )
    doTarget( geom_params )
