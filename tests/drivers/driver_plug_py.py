import mdi
import sys
import argparse
from mpi4py import MPI

use_mpi4py = True

def code_for_plugin_instance(mpi_comm, mdi_comm, class_object):
    mpi_rank = 0
    if use_mpi4py:
        mpi_rank = mpi_comm.Get_rank()

    # Determine the name of the engine
    mdi.MDI_Send_Command("<NAME", mdi_comm)
    name = mdi.MDI_Recv(mdi.MDI_NAME_LENGTH, mdi.MDI_CHAR, mdi_comm)

    if mpi_rank == 0:
        print(" Engine name: " + str(name))

    # Determine the number of atoms
    mdi.MDI_Send_Command("<NATOMS", mdi_comm)
    natoms = mdi.MDI_Recv(1, mdi.MDI_INT, mdi_comm)

    if mpi_rank == 0:
        print(" natoms: " + str(natoms))

    # Get the energy
    mdi.MDI_Send_Command("<ENERGY", mdi_comm)
    energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, mdi_comm)

    if mpi_rank == 0:
        print(" energy: " + str(energy))

    # Send the "EXIT" command to the engine
    mdi.MDI_Send_Command("EXIT", mdi_comm)

    return 0


if __name__ == "__main__":

    # Parse command-line arguments
    mdi_options = None
    plugin_name = None
    for iarg in range( len(sys.argv) ):
        if sys.argv[iarg] == "--mdi":
            mdi_options = sys.argv[iarg+1]
            iarg += 1
        elif sys.argv[iarg] == "--plugin_name":
            plugin_name = sys.argv[iarg+1]
            iarg += 1
    if mdi_options is None:
        raise Exception("-mdi command-line option was not provided")
    if plugin_name is None:
        raise Exception("-plugin_name command-line option was not provided")

    # Initialize the MDI Library
    mdi.MDI_Init( mdi_options )

    mpi_world = None
    world_rank = 0
    if use_mpi4py:
        mpi_world = mdi.MDI_MPI_get_world_comm()
        world_rank = mpi_world.Get_rank()

    # Confirm that this code is being used as a driver
    role = mdi.MDI_Get_Role()
    if not role == mdi.MDI_DRIVER:
        raise Exception("Must run driver_py.py as a DRIVER")

    if True:
        if world_rank == 0:
            print("I am engine instance: 1")

        # Launch an instance of the engine library
        mdi.MDI_Launch_plugin(plugin_name,
                              "-mdi \"-name MM -role ENGINE -method LINK\"",
                              mpi_world,
                              code_for_plugin_instance,
                              None)

        # Launch an instance of the engine library
        mdi.MDI_Launch_plugin(plugin_name,
                              "-mdi \"-name MM -role ENGINE -method LINK\"",
                              mpi_world,
                              code_for_plugin_instance,
                              None)
                              