import os
import sys
import math
import numpy

sys.path.append( "/home/greg/apps/seacas/lib" )
import exodus

def doIndenter():
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

def doTarget():
    layerDepth = 5.0

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
        if nCoords[1][i] < -1.0 * layerDepth:
            meshSize[i] = ( dist[i] - layerDepth ) / ( maxDist - layerDepth )
    
    E.put_time( 1, 0.0 )
    exodus.add_variables( E, nodal_vars = ["meshSize"] )
    E.put_node_variable_values( "meshSize", 1, meshSize )
    E.close()

if __name__ == "__main__":
    doIndenter()
    doTarget()
