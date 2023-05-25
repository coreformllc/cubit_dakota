#!python
from ast import arguments
import os
import sys
import subprocess
import numpy
from math import *

# Local imports
import spherical_nanoindenter

# Import Cubit Python
pathToCubit = "/opt/Coreform-Cubit-2023.4/bin"
sys.path.append( pathToCubit )
import cubit
cubit.init( [ "cubit", "-nobanner", "-nographics", "-commandplugindir", "/home/gvernon2/cf/master/build/bin/Release" ] )

# Import Exodus Python
sys.path.append( "/home/greg/apps/seacas/lib" )
import exodus

def main( paramFile, objFile ):
    params = readParamFile( paramFile )
    status = build_model( params )
    status = submit_moose( )
    obj = compute_objective( )
    con = compute_constraint( )
    write_results( { "Objective": obj, "Constraint": con }, objFile )

def readParamFile( paramFile ):
    f = open( paramFile, 'r' )
    fLines = f.readlines()
    params = { "tip_radius":     float( fLines[0].strip() ),
               "shaft_radius_ratio":   float( fLines[1].strip() ),
               "wedge_angle":    float( fLines[2].strip() ) }
    # Fixed values
    params[ "shaft_standoff" ] = 10
    params[ "target_width" ] = 60
    params[ "target_height" ] = 60
    return params

def build_model( params ):
    spherical_nanoindenter.main( params )

def submit_moose( ):
    mpi = "/home/greg/mambaforge3/envs/moose/bin/mpiexec"
    executable = "/home/greg/projects/struct_mech/struct_mech-opt"
    argument = "-i indenter_power_law.i"
    status = subprocess.run( f"{mpi} -np 4 {executable} {argument} > moose.out 2>moose.err", shell=True, check=True )

def compute_objective( ):
    filename = "indenter_power_law_out.e"
    E = exodus.exodus( filename, array_type="numpy", mode="r" )
    target_depth = E.get_global_variable_values( "target_depth" )
    E.close()
    objective = abs( -1.5 - target_depth[-1] )
    return objective

def compute_constraint( ):
    filename = "indenter_power_law_out.e"
    E = exodus.exodus( filename, array_type="numpy", mode="r" )
    reaction_force = E.get_global_variable_values( "react_y" )
    E.close()
    constraint = max( reaction_force )
    return constraint

def write_results( results, resFile ):
    f = open( resFile, "w+" )
    f.write( f"final_depth {results['Objective']}\n" )
    f.write( f"reaction_force {results['Constraint']}\n" )
    f.close()

def list_to_str( input_list ):
    return " ".join( [ str(val) for val in input_list ] )

if __name__ == "__main__":
    print( sys.argv )
    paramFile = sys.argv[1]
    objFile = sys.argv[2]
    main(paramFile, objFile)