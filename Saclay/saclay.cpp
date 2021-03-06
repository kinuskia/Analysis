#include <iostream>
#include <vector>
//#include <gsl/gsl_vector.h>

#include "model.hpp"
#include "../auxiliary/fbdecomposition.hpp" // load after (!) model.hpp
#include "../auxiliary/to_file.hpp"
#include "../auxiliary/to_size_t.hpp"

#include <ctime>

/*
Idea: In the file "model.hpp" one specifies the position space one-point
and two-point correlation function of an arbitrary initial-state model.
Here, t
*/

int main (int argc, char* argv[]) // comand-line input: centrality_min, centrality_max, # grid points for r-integration, # gridpoints azimuthal direction, output location, infrared cutoff
{
	typedef std::size_t size_type;
	typedef double number_type;

	
	size_type centrality_min = to_size_t(argv[1]);
	size_type centrality_max = to_size_t(argv[2]);
	size_type n_grid = to_size_t(argv[3]);
	size_type n_azim = to_size_t(argv[4]);
	std::string destination = argv[5];
	number_type m_IR = std::stod(argv[6]);
	std::string centrality = std::to_string(centrality_min) + "-" + std::to_string(centrality_max);

	// Set up initial-state model
	Model<number_type> model(m_IR, 6.624, 0.549, 0.);
	model.initialize_W("../Saclay_simplified/output/"+centrality+"/weight_functions_magma_"+centrality+".txt");
	model.initialize_T();
	// const gsl_interp2d_type* xy_interpolation_method = gsl_interp2d_bicubic;
	// model.initialize_OnePoint("../output/profiles_averaged_"+centrality+".txt", 100, xy_interpolation_method, 10, 0.2);

	// Set up Fourier-Bessel decomposition object
	// with rMax = 10 as maximal radial integration length
	FBDecomposition<number_type> decomposition(model, 9.604+0*1.*8.604, centrality_min);
	
	decomposition.get_impact_parameter_distribution("../output/percentiles_b.txt");
	decomposition.initialize();

	// set number of radial grid points per dimension
	decomposition.set_N_discret(n_grid);

	// set # gridpoints for FFT
	decomposition.set_Nm_(n_azim);

	
	// Compute <e_l1^(m)e_l2^(-m)> as a function of l
	int mMax = 10; //4
	int lMax = 20; //10
	decomposition.fill_background_bar_for(mMax, lMax);
	decomposition.print_background_bar(destination + "/background_coeffs_CGC_" + centrality + ".txt");
	number_type counter = 0;
	number_type progress_steps = 100;

	std::time_t start = std::time(nullptr);
	bool estimate_given = false;
	size_type nb_steps = (mMax+1)*lMax*lMax;

	// number_type current = decomposition.TwoMode_fast(1, 9, -1, 9);
	// std::cout << current << "\n";
	


	for (int m = mMax; m >= 0; --m) 
	{
		// if ((m != 1)) // DELETE AFTERWARDS
		// {
		// 	continue;
		// }
		// save result in matrix
		gsl_matrix* result = gsl_matrix_alloc(lMax, lMax);
		for (int l1 = 1; l1 <= lMax; ++l1)
		{
			for (int l2 = 1; l2 <= lMax; ++l2)
			{
				// ///////////////////////////////////////////////////////
				// if ( (m <= 4) && (l1 < 10 && l2 < 10) )
				// {
				// 	gsl_matrix_set(result, l1-1, l2-1, 0.0);
				// 	continue;
				// }
				// ///////////////////////////////////////////////////////
				// if (l1 != l2)
				// {
				// 	gsl_matrix_set(result, l1-1, l2-1, 0.0);
				// 	continue;
				// }

				if (l1 > l2) // make use of symmetry
				{
					continue;
				}

				std::cout << "m=" << m << ", l1= " << l1 << ", l2=" << l2 << "\n";
				// Print progress
				for (size_type i = 1; i < progress_steps; ++i)
				{
					if (counter == size_type(i*nb_steps/progress_steps))
					{
						std::cout << "Progress: " << size_type(i*100./progress_steps) << "%" << "\n";
					}
				}
				// After 60 s: estimate total computation time:
				std::time_t end = std::time(nullptr);
				number_type diff = end - start;
				if ( (diff > 60) && !estimate_given)
				{
					number_type expected_duration = 1.0*nb_steps * diff / counter / 60;
					std::cout << "Computation time in min: " << expected_duration << "\n";
					estimate_given = true;
				}
				number_type current = decomposition.TwoMode_fast2(m, l1, -m, l2, centrality_min);	
				gsl_matrix_set(result, l1-1, l2-1, current);

				// make use of symmetry
				gsl_matrix_set(result, l2-1, l1-1, current);

				counter++;
			}
			
		}

		// save result to text file
		std::string filename = destination + "/two_point_random_connected_m_";
		filename += std::to_string(m);
		//filename += "_test";
		filename += ".txt";

		to_file(filename, result);

		gsl_matrix_free(result);
	}

	

	// report total calculation time
	std::time_t end = std::time(nullptr);
	number_type diff = 1.0*(end - start)/60;
	std::cout << "Total calculation time in min : " << diff << "\n";





	return 0;
}