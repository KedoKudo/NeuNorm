
import unittest
import numpy as np
import os
from PIL import Image

from NeuNorm.normalization import Normalization
from NeuNorm.roi import ROI


class TestLoading(unittest.TestCase):
    
    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../data/'))
        
    def test_dict_initialized(self):
        '''assert image, ob and df dicts are correctly initialized'''
        o_norm = Normalization()
        data = o_norm.data
        dict_image = o_norm.dict_image
        self.assertEqual([], dict_image['data'])
        self.assertEqual([], dict_image['file_name'])
        self.assertEqual([], data['sample']['data'])
        self.assertEqual([], data['sample']['file_name'])
        
        dict_ob = o_norm.dict_ob
        self.assertEqual([], dict_ob['data'])
        self.assertEqual([], dict_ob['file_name'])
        self.assertEqual([], data['ob']['data'])
        self.assertEqual([], data['ob']['file_name'])

        dict_df = o_norm.dict_df
        self.assertEqual([], dict_df['data'])
        self.assertEqual([], dict_df['file_name'])
        self.assertEqual([], data['df']['data'])
        self.assertEqual([], data['df']['file_name'])
        
    def test_same_number_of_images_loaded_in_sample_and_ob(self):
        '''assert sample and ob have the same number of images loaded'''
        sample_tif_file_1 = self.data_path + '/tif/sample/image001.tif'
        sample_tif_file_2 = self.data_path + '/tif/sample/image002.tif'
        o_norm = Normalization()
        o_norm.load(file=sample_tif_file_1, data_type='sample')
        o_norm.load(file=sample_tif_file_2, data_type='sample')
        ob_tif_file_1 = self.data_path + '/tif/ob/ob001.tif'
        o_norm.load(file=ob_tif_file_1, data_type='ob')
        self.assertRaises(IOError, o_norm.normalization)  

    def test_loading_bad_single_files(self):
        '''assert error is raised when inexisting file is given'''
        bad_tiff_file_name = 'bad_tiff_file_name.tiff'
        o_norm = Normalization()
        self.assertRaises(OSError, o_norm.load, bad_tiff_file_name, '', 'sample')
        self.assertRaises(OSError, o_norm.load, bad_tiff_file_name, '', 'ob')
        self.assertRaises(OSError, o_norm.load, bad_tiff_file_name, '', 'df')
        bad_fits_file_name = 'bad_fits_file_name.fits'
        o_norm = Normalization()
        self.assertRaises(OSError, o_norm.load, bad_fits_file_name, '', 'sample')
        self.assertRaises(OSError, o_norm.load, bad_fits_file_name, '', 'ob')
        self.assertRaises(OSError, o_norm.load, bad_fits_file_name, '', 'df')
        bad_h5_file_name = 'bad_h5_file_name.h5'
        self.assertRaises(OSError, o_norm.load, bad_h5_file_name, '', 'sample')
        self.assertRaises(OSError, o_norm.load, bad_h5_file_name, '', 'ob')
        self.assertRaises(OSError, o_norm.load, bad_h5_file_name, '', 'df')
        
    def test_loading_good_single_file(self):
        '''assert sample, ob and df single file correctly loaded'''
        # tiff
        sample_tif_file = self.data_path + '/tif//sample/image001.tif'
        o_norm = Normalization()
        o_norm.load(file=sample_tif_file, data_type='sample')
        _expected_data = np.ones([5,5])
        _expected_data[0,0] = 5
        _expected_data[:,2] = 2
        _expected_data[:,3] = 3
        _expected_data[:,4] = 4
        _loaded_data = o_norm.data['sample']['data']
        self.assertTrue((_expected_data == _loaded_data).all())
        _expected_name = sample_tif_file
        _loaded_name = o_norm.data['sample']['file_name'][0]
        self.assertTrue(_expected_name == _loaded_name)

        # fits
        sample_fits_file = self.data_path + '/fits//sample/image001.fits'
        o_norm = Normalization()
        o_norm.load(file=sample_fits_file, data_type='sample')
        _expected_data = np.ones([5,5])
        _expected_data[0,0] = 5
        _expected_data[:,2] = 2
        _expected_data[:,3] = 3
        _expected_data[:,4] = 4
        _loaded_data = o_norm.data['sample']['data']
        self.assertTrue((_expected_data == _loaded_data).all())
        _expected_name = sample_fits_file
        _loaded_name = o_norm.data['sample']['file_name'][0]
        self.assertTrue(_expected_name == _loaded_name)
        
    def test_loading_good_several_single_files(self):
        '''assert sample, ob and df multi files correctly loaded'''
        # tiff
        sample_tif_file_1 = self.data_path + '/tif//sample/image001.tif'
        sample_tif_file_2 = self.data_path + '/tif/sample/image002.tif'
        ob_tif_file_1 = self.data_path + '/tif/ob/ob001.tif'
        o_norm = Normalization()
        o_norm.load(file=sample_tif_file_1, data_type='sample')
        o_norm.load(file=sample_tif_file_2, data_type='sample')
        o_norm.load(file=ob_tif_file_1, data_type='ob')
        
        # sample 0
        _expected_data_1 = np.ones([5,5])
        _expected_data_1[0,0] = 5
        _expected_data_1[:,2] = 2
        _expected_data_1[:,3] = 3
        _expected_data_1[:,4] = 4
        _loaded_data_1 = o_norm.data['sample']['data'][0]
        self.assertTrue((_expected_data_1 == _loaded_data_1).all())
        _expected_name_1 = sample_tif_file_1
        _loaded_name_1 = o_norm.data['sample']['file_name'][0]
        self.assertTrue(_expected_name_1 == _loaded_name_1)
        
        # sample 1
        _expected_data_2 = np.ones([5,5])
        _expected_data_2[0,0] = 5
        _expected_data_2[:,2] = 2
        _expected_data_2[:,3] = 3
        _expected_data_2[:,4] = 4
        _loaded_data_2 = o_norm.data['sample']['data'][1]
        self.assertTrue((_expected_data_2 == _loaded_data_2).all())
        _expected_name_2 = sample_tif_file_2
        _loaded_name_2 = o_norm.data['sample']['file_name'][1]
        self.assertTrue(_expected_name_2 == _loaded_name_2)        
 
        # ob 0
        _expected_data_1 = np.ones([5,5])
        _expected_data_1[0,0] = 5
        _loaded_data_1 = o_norm.data['ob']['data'][0]
        self.assertTrue((_expected_data_1 == _loaded_data_1).all())
        
        # fits
        sample_fits_file_1 = self.data_path + '/fits//sample/image001.fits'
        sample_fits_file_2 = self.data_path + '/fits/sample/image002.fits'
        o_norm = Normalization()
        o_norm.load(file=sample_fits_file_1, data_type='sample')
        o_norm.load(file=sample_fits_file_2, data_type='sample')
    
        _expected_data_1 = np.ones([5,5])
        _expected_data_1[0,0] = 5
        _expected_data_1[:,2] = 2
        _expected_data_1[:,3] = 3
        _expected_data_1[:,4] = 4
        _loaded_data_1 = o_norm.data['sample']['data'][0]
        self.assertTrue((_expected_data_1 == _loaded_data_1).all())
        _expected_name_1 = sample_fits_file_1
        _loaded_name_1 = o_norm.data['sample']['file_name'][0]
        self.assertTrue(_expected_name_1 == _loaded_name_1)
    
        _expected_data_2 = np.ones([5,5])
        _expected_data_2[0,0] = 5
        _expected_data_2[:,2] = 2
        _expected_data_2[:,3] = 3
        _expected_data_2[:,4] = 4
        _loaded_data_2 = o_norm.data['sample']['data'][1]
        self.assertTrue((_expected_data_2 == _loaded_data_2).all())
        _expected_name_2 = sample_fits_file_2
        _loaded_name_2 = o_norm.data['sample']['file_name'][1]
        self.assertTrue(_expected_name_2 == _loaded_name_2)                 
    
    def test_all_images_names_retrieved_from_folder(self):
        '''assert list_of images are correctly loaded when retrieved from folder'''
        # tif
        path = self.data_path + '/tif/sample'
        o_norm = Normalization()
        o_norm.load(folder=path, data_type='sample')
        list_of_files = ['image001.tif', 'image002.tif', 'image003.tif']
        list_of_files_expected = [os.path.join(path, _file) for _file in list_of_files]
        list_of_files_retrieved = o_norm.data['sample']['file_name']
        self.assertTrue(list_of_files_expected == list_of_files_retrieved)
        
        #fits
        path = self.data_path + '/fits/sample'
        o_norm = Normalization()
        o_norm.load(folder=path, data_type='sample')
        list_of_files = ['image001.fits', 'image002.fits', 'image003.fits']
        list_of_files_expected = [os.path.join(path, _file) for _file in list_of_files]
        list_of_files_retrieved = o_norm.data['sample']['file_name']
        self.assertTrue(list_of_files_expected == list_of_files_retrieved)
        
    def test_error_raised_when_data_size_do_not_match(self):
        '''assert IOError raised when data of a same type do not match in size'''
        # sample
        image1 = self.data_path + '/tif/sample/image001.tif'
        image2 = self.data_path + '/different_format/image001_4_by_4.tif'
        o_norm = Normalization()
        o_norm.load(file=image1)
        self.assertRaises(IOError, o_norm.load, file=image2)

        # ob
        ob1 = self.data_path + '/tif/ob/ob001.tif'
        ob2 = self.data_path + '/different_format/ob001_4_by_4.tif'
        o_norm = Normalization()
        o_norm.load(file=ob1)
        self.assertRaises(IOError, o_norm.load, file=ob2)
        
        # df
        df1 = self.data_path + '/tif/df/df001.tif'
        df2 = self.data_path + '/different_format/df001_4_by_4.tif'
        o_norm = Normalization()
        o_norm.load(file=df1)
        self.assertRaises(IOError, o_norm.load, file=df2)        

    def test_loading_new_data_not_allowed_if_algorithm_already_run(self):
        '''assert error raises when loading new data on data already manipulated'''
        # tiff
        sample_tif_file = self.data_path + '/tif/sample/image001.tif'
        ob_tif_file = self.data_path +'/tif/ob/ob001.tif'
        o_norm = Normalization()
        o_norm.load(file=sample_tif_file, data_type='sample')
        o_norm.load(file=ob_tif_file, data_type='ob')
        o_norm.normalization()
        new_sample_tif_file = self.data_path + '/tif/sample/image002.tif'
        self.assertRaises(IOError, o_norm.load, file=new_sample_tif_file)