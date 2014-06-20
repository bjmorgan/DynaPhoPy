import numpy as np
import matplotlib.pyplot as plt
import correlation
import Functions.reading as reading
import Functions.projection as projection
import Functions.eigenvectors as eigen
import Functions.peaksearch as peaksearch
import phonopy.file_IO as file_IO
import Functions.phonopy_interface as pho_interface
import Functions.correlate as correlate

print("Program start")

#Parameters definition section (one parameter left)
q_vector = np.array ([1.5,0.5])

#Reading structure
#structure = reading.read_from_file_structure('/home/abel/VASP/Si-test/OUTCAR')

#Reading force constants from vasprun.xml
#force_constants = get_force_constants_from_file('/home/abel/VASP/Si-test/FORCE_CONSTANTS')
#force_constants = file_IO.read_force_constant_vasprun_xml('/home/abel/VASP/Si-test/vasprun.xml')[0]
#structure.set_force_constants(force_constants)

#Reading trajectory from test files
#trajectory = reading.read_from_file_trajectory('/home/abel/VASP/Si-dynamic_300/OUTCAR',structure)


#Test things
trajectory = reading.read_from_file_test()
eigenvectors, original_frequencies = eigen.get_eigenvectors_test(trajectory.structure)


plt.suptitle('Trajectory')
plt.plot(trajectory.get_time().real,trajectory.get_trajectory()[:,1].real)
plt.show()

#Getting eigenvectors from somewhere
#eigenvectors, original_frequencies = pho_interface.obtain_eigenvectors_from_phonopy(trajectory.structure,q_vector)

#Plot energy
plt.suptitle('Energy')
#plt.plot(trajectory.get_time().real,trajectory.get_energy().real)
#plt.show()



#Test things
trajectory = reading.read_from_file_test()
eigenvectors, original_frequencies = eigen.get_eigenvectors_test(trajectory.structure)


print('Original frequencies')
print(original_frequencies)

#Projection onto unit cell
vc = projection.project_onto_unit_cell(trajectory,q_vector)
plt.suptitle('Projection onto unit cell')
plt.plot(trajectory.get_time().real,vc[:,0,:].real)
plt.show()


#Projection onto phonon coordinates
vq = projection.project_onto_phonon(vc,eigenvectors)
plt.suptitle('Projection onto phonon')
plt.plot(trajectory.get_time().real,vq[:,2:4].real)
plt.show()


#Noise generation (for test only)
#for i in range(vq.shape[0]):
#    vq[i,:] += random.uniform(-0.5,0.5)


# Correlation section (working on..)
print ('Correlation')

test_frequencies_range = np.array([0.1*i + 0.1 for i in range (100)])


correlation_vector =  correlate.get_correlation_spectrum(vq,trajectory,test_frequencies_range)


#Search for frequencies
frequencies = peaksearch.get_frequencies_from_correlation(correlation_vector,test_frequencies_range)
print 'Frequencies:',frequencies


#Dynamical Matrix section
print('Matrix section\n')


print('Final Dynamical Matrix')
new_frequencies, new_eigenvectors, dynamical_matrix = eigen.build_dynamical_matrix(trajectory.structure,frequencies,eigenvectors)
print(dynamical_matrix)


print('\n')
print('EigenVectors & EigenValues')
print(new_frequencies)

exit()

