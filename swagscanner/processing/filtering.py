import os
import pcl
from swagscanner.utils.file import FileSaver


class Filtering():
    ''' provide the tools for filtering

    '''

    def __init__(self, input_folder_path, write_folder_path, file_saver=None):
        self.input_folder_path = input_folder_path
        if file_saver is None:
            self.write_folder_path = write_folder_path
            self.file_saver = FileSaver(folder_path=self.write_folder_path)

        else:
            self.write_folder_path = write_folder_path
            self.file_saver = file_saver
            self.file_saver.write_folder_path = write_folder_path

    def voxel_grid_filtering(self, point_cloud, file_name):

        sor = point_cloud.make_voxel_grid_filter()
        sor.set_leaf_size(0.0005, 0.0005, 0.0005)
        point_cloud_filtered = sor.filter()

        self.file_saver.save_point_cloud(point_cloud=point_cloud_filtered,
                                         file_name=file_name)
        # TODO: log this

    def filter_all(self):
        '''Filter all the pointcloud files inside the clipped folder
        then save them to the filtered folder

        '''

        cloud_list = self.file_saver.get_cloud_list(self.input_folder_path)

        # filter everything
        for cloud in cloud_list:
            file_name = os.path.splitext(os.path.basename(cloud))[0]
            cloud = pcl.load(cloud)
            self.voxel_grid_filtering(cloud, file_name)


def main():
    filtering = Filtering(input_folder_path='/Users/seanngpack/Programming Stuff/Projects/scanner_files/7/',
                          write_folder_path='/Users/seanngpack/Programming Stuff/Projects/scanner_files/7/filtered')
    filtering.filter_all()


if __name__ == "__main__":
    main()
