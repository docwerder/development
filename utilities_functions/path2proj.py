import re

class Path2Proj(object):
    project_pattern6 = "(\/proj[a-z0-9]{1}\/[0-9]{5}\/[0-9]{2}[a-z0-9]{6}\/[a-z]{2}_[a-z]{6}\/[a-z]{9}\/[0-9a-z-_]*\/)"

    region_number = ""  # 'proj0'
    project_number = ""  # '12542'
    lineshort_name = ""  # '30305306'

    has_project_info = False

    def __init__(self, path_or_level: str):
        find_results = re.findall(self.project_pattern6, path_or_level.lower().replace("\\", "/").replace(".", "/") + "/")
        if len(find_results) > 0:
            parts = find_results[0].strip("/").split("/")  # we take the first find result only
            assert len(parts) == 6, "Internal error, length of parts does not match"
            self.region_number = parts[0]  # 'proj0'
            self.project_number = parts[1]  # '12542'
            self.lineshort_name = parts[2]  # '30305306'
            self.ap_xarray_label = parts[3]  # would be "AP_xarray", which is not relevant for this case...
            self.anomalies_label = parts[4] # 'anomalies'
            self.single_anomaly_label = parts[5]  # 'plin', or "melo" etc...

            self.has_project_info = True
            return
#
#     ''' This class extracts ROSEN project info from a filesystem path or PDW level path.
#         It searches for pattern like proj0\12345\28LAUREC . In words, there must be a part named region_number pattern starting
#         with "proj" and a single digit (0-9) (example proj8) or another character (projz), then a slash, backslash, or dot,
#         followed by the project_number, which has 5 digits, then again a slash, backslash, or dot, and finally the lineshort_name
#         which has two leading digits and then exactly 6 characters (example 20LINTRU).
#         The class works case-insensitive and provides all information in lower case.
#
#         provides:
#
#         has_project_info : bool
#         region_number : str , example 'proj7'
#         project_number : str , example '12542'
#         lineshort_name : str , example '30GORGON'
#
#         example:
#             fs_path = r"//linfile1/groups/EMAT_evaluation_data/CombEvalDataWarehouse\proj0/12542/30305306/AP_xarray/anomalies\lin\14039.nc"
#             p = Path2Proj(fs_path)
#             if not p.has_project_info:
#                 print("no project info found")
#             else:
#                 print(p.lineshort_name)
#
#
#     '''
#     #project_pattern3 = "(\/proj[a-z0-9]{1}\/[0-9]{5}\/[0-9]{2}[a-z0-9]{6}\/)"
#     #project_pattern4 = "(\/proj[a-z0-9]{1}\/[0-9]{5}\/[0-9]{2}[a-z0-9]{6}\/[a-z0-9_]{7}r[1-9]{1}[a-z]{2}\/)"
#     #project_pattern5 = "(\/proj[a-z0-9]{1}\/[0-9]{5}\/[0-9]{2}[a-z0-9]{6}_r[1-9]{1}[a-z]{2}\/)"
#     project_pattern6 = "(\/proj[a-z0-9]{1}\/[0-9]{5}\/[0-9]{2}[a-z0-9]{6}\/[a-z]{2}_[a-z]{6}\/[a-z]{9}\/[0-9a-z-_]*\/)"
#
#     find_results = re.findall(self.project_pattern6, path_or_level.lower().replace("\\", "/").replace(".", "/") + "/")
#
#     if len(find_results) > 0:
#         parts = find_results[0].strip("/").split("/")  # we take the first find result only
#         assert len(parts) == 6, "Internal error, length of parts does not match"
#         self.region_number = parts[0]  # 'proj0'
#         self.project_number = parts[1]  # '12542'
#         self.lineshort_name = parts[2]  # '30305306'
#         self.ap_xarray_label = parts[3]  # would be "AP_xarray", which is not relevant for this case...
#         self.anomalies_label = parts[4] # 'anomalies'
#         self.single_anomaly_label = parts[5]  # 'plin', or "melo" etc...
#
#         self.has_project_info = True
#         return
#

        # find_results = re.findall(self.project_pattern5, path_or_level.lower().replace("\\", "/").replace(".", "/") + "/")
        # if len(find_results) > 0:
        #     parts = find_results[0].strip("/").split("/")  # we take the first find result only
        #     assert len(parts) == 3, "Internal error, length of parts does not match"
        #     self.region_number = parts[0]  # 'proj0'
        #     self.project_number = parts[1]  # '12542'
        #     self.lineshort_name = parts[2]  # '30305306'
        #     self.has_project_info = True
        #     return

        # find_results = re.findall(self.project_pattern4, path_or_level.lower().replace("\\", "/").replace(".", "/") + "/")
        # if len(find_results)>0:
        #     parts = find_results[0].strip("/").split("/") # we take the first find result only
        #     assert len(parts)==4, "Internal error, length of parts does not match"
        #     self.region_number = parts[0]  # 'proj0'
        #     self.project_number = parts[1] # '12542'
        #     self.lineshort_name = parts[2] # '30305306'
        #     self.run_number = parts[3]
        #     self.has_project_info = True
        #     return
        # find_results = re.findall(self.project_pattern3, path_or_level.lower().replace("\\", "/").replace(".", "/") + "/")
        # if len(find_results)>0:
        #     parts = find_results[0].strip("/").split("/") # we take the first find result only
        #     assert len(parts)==3, "Internal error, length of parts does not match"
        #     self.region_number = parts[0]  # 'proj0'
        #     self.project_number = parts[1] # '12542'
        #     self.lineshort_name = parts[2] # '30305306'
        #     self.has_project_info = True
        #     return

class Path2Proj_xarray(object):
    ''' This class extracts ROSEN project info from a filesystem path or PDW level path.
            It searches for pattern like proj0\12345\28LAUREC . In words, there must be a part named region_number pattern starting
            with "proj" and a single digit (0-9) (example proj8) or another character (projz), then a slash, backslash, or dot,
            followed by the project_number, which has 5 digits, then again a slash, backslash, or dot, and finally the lineshort_name
            which has two leading digits and then exactly 6 characters (example 20LINTRU).
            The class works case-insensitive and provides all information in lower case.
            Special class for dealing with the folder "xarray"

            provides:

            has_project_info : bool
            region_number : str , example 'proj7'
            project_number : str , example '12542'
            lineshort_name : str , example '30GORGON'

            example:
                fs_path = r"//linfile1/groups/EMAT_evaluation_data/CombEvalDataWarehouse\proj0/12542/30305306/AP_xarray/anomalies\lin\14039.nc"
                p = Path2Proj(fs_path)
                if not p.has_project_info:
                    print("no project info found")
                else:
                    print(p.lineshort_name)


        '''
    project_pattern7 = "(\/proj[a-z0-9]{1}\/[0-9]{5}\/[0-9]{2}[a-z0-9]{6}\/[a-z]{2}_[a-z]{6}\/)"

    region_number = ""  # 'proj0'
    project_number = ""  # '12542'
    lineshort_name = ""  # '30305306'
    ap_xarray_label = ""
    has_project_info = False

    def __init__(self, path_or_level: str):
        """
        :param path_or_level (str): a filesystem path or a PDW level path
                                    i.e. "protoptypes.schnipp.schnapp.proj0.12345.28gorgon.dha.dings.bumms"
                                    or "c:\test\schnipp\schnapp/proj0\12345/28gorgon\dha\dings\bumms"
        """
        find_results = re.findall(self.project_pattern7,
                                  path_or_level.lower().replace("\\", "/").replace(".", "/") + "/")
        if len(find_results) > 0:
            parts = find_results[0].strip("/").split("/")  # we take the first find result only
            assert len(parts) == 4, "Internal error, length of parts does not match"
            self.region_number = parts[0]  # 'proj0'
            self.project_number = parts[1]  # '12542'
            self.lineshort_name = parts[2]  # '30305306'
            self.ap_xarray_label = parts[3]  # would be "AP_xarray",
            # self.anomalies_label = parts[4]  # 'anomalies'
            # self.single_anomaly_label = parts[5]  # 'plin', or "melo" etc...

            self.has_project_info = True
            return



    def __str__(self):
        return f"has_project_infos: {self.has_project_info}, region_number: {self.region_number}, project_number: {self.project_number}, lineshot_name:{self.lineshort_name}"

    def to_dict(self):
        return {"has_project_info": self.has_project_info, "region_number": self.region_number, "project_number": self.project_number, "lineshot_name":self.lineshort_name}

class Path2Proj_anomalies(object):
    ''' This class extracts ROSEN project info from a filesystem path or PDW level path.
        It searches for pattern like proj0\12345\28LAUREC . In words, there must be a part named region_number pattern starting
        with "proj" and a single digit (0-9) (example proj8) or another character (projz), then a slash, backslash, or dot,
        followed by the project_number, which has 5 digits, then again a slash, backslash, or dot, and finally the lineshort_name
        which has two leading digits and then exactly 6 characters (example 20LINTRU).
        The class works case-insensitive and provides all information in lower case.
    '''
    #         example:
    #             fs_path = r"//linfile1/groups/EMAT_evaluation_data/CombEvalDataWarehouse\proj0/12542/30305306/AP_xarray/anomalies\lin\14039.nc"
    #             p = Path2Proj(fs_path)
    #             if not p.has_project_info:
    #                 print("no project info found")
    #             else:
    #                 print(p.lineshort_name)

   #project_pattern4 = "(\/proj[a-z0-9]{1}\/[0-9]{5}\/[0-9]{2}[a-z0-9]{6}\/[a-z0-9_]{7}r[1-9]{1}[a-z]{2}\/)"
    project_pattern4 = "(\/proj[a-z0-9]{1}\/[0-9]{5}\/[0-9]{2}[a-z0-9]{6}\/[A-Za-z]{2}_[a-z]{6}\/[a-z]{9}\/)"
    region_number = ""  # 'proj0'
    project_number = ""  # '12542'
    lineshort_name = ""  # '30305306'

    has_project_info = False

    def __init__(self, path_or_level: str):
        find_results = re.findall(self.project_pattern4, path_or_level.lower().replace("\\", "/").replace(".", "/") + "/")
        if len(find_results) > 0:
            parts = find_results[0].strip("/").split("/") # we take the first find result only
            assert len(parts)==5, "Internal error, length of parts does not match"
            self.region_number = parts[0]  # 'proj0'
            self.project_number = parts[1] # '12542'
            self.lineshort_name = parts[2] # '30305306'
            self.ap_xarray_label = parts[3] # 'AP_array'
            self.anomalies_label = parts[4] # 'anomalies'
            self.has_project_info = True
            return

class Path2Proj_anomalies_srh5_crawler(object):
    ''' This class extracts ROSEN project info from a filesystem path or PDW level path.
        It searches for pattern like proj0\12345\28LAUREC . In words, there must be a part named region_number pattern starting
        with "proj" and a single digit (0-9) (example proj8) or another character (projz), then a slash, backslash, or dot,
        followed by the project_number, which has 5 digits, then again a slash, backslash, or dot, and finally the lineshort_name
        which has two leading digits and then exactly 6 characters (example 20LINTRU).
        The class works case-insensitive and provides all information in lower case.
    '''
    #         example:
    #             fs_path = r"//linfile1/groups/EMAT_evaluation_data/CombEvalDataWarehouse\proj0/12542/30305306/AP_xarray/anomalies\lin\14039.nc"
    #             p = Path2Proj(fs_path)
    #             if not p.has_project_info:
    #                 print("no project info found")
    #             else:
    #                 print(p.lineshort_name)
    #print('new one')
    project_pattern7 = "(\/proj[a-z0-9]{1}\/[0-9]{5}\/[0-9]{2}[a-z0-9]{6}\/[a-z]{2}_[a-z]{6}_[a-z0-9]{4}_[a-z0-9]{7}\/)"
    region_number = ""  # 'proj0'
    project_number = ""  # '12542'
    lineshort_name = ""  # '30305306'

    has_project_info = False

    def __init__(self, path_or_level: str):
        find_results = re.findall(self.project_pattern7,
                                  path_or_level.lower().replace("\\", "/").replace(".", "/") + "/")
        if len(find_results) > 0:
            parts = find_results[0].strip("/").split("/")  # we take the first find result only
            assert len(parts) == 4, "Internal error, length of parts does not match"
            self.region_number = parts[0]  # 'proj0'
            self.project_number = parts[1]  # '12542'
            self.lineshort_name = parts[2]  # '30305306'
            self.ap_xarray_label = parts[3]  # would be "AP_xarray_srh5_crawler",
            self.run_number = parts[3]
            self.has_project_info = True
            return

class Path2ProjAnomaliesGeneral(object):
    ''' This class extracts ROSEN project info from a filesystem path or PDW level path.
        It searches for pattern like proj0\12345\28LAUREC . In words, there must be a part named region_number pattern starting
        with "proj" and a single digit (0-9) (example proj8) or another character (projz), then a slash, backslash, or dot,
        followed by the project_number, which has 5 digits, then again a slash, backslash, or dot, and finally the lineshort_name
        which has two leading digits and then exactly 6 characters (example 20LINTRU).
        The class works case-insensitive and provides all information in lower case.
    '''
    #         example:
    #             fs_path = r"//linfile1/groups/EMAT_evaluation_data/CombEvalDataWarehouse\proj0/12542/30305306/AP_xarray/anomalies\lin\14039.nc"
    #             p = Path2Proj(fs_path)
    #             if not p.has_project_info:
    #                 print("no project info found")
    #             else:
    #                 print(p.lineshort_name)

    #project_pattern = "(\/proj[a-z0-9]{1}\/[0-9]{5}\/[0-9]{2}[a-z0-9]{6}\/[a-z]{2}_[a-z]{6}_[a-z0-9]{4}_[a-z0-9]{7}\/)"

    #project_pattern = "(\/proj[a-z0-9]{1}\/[0-9]{5}\/[0-9]{2}[a-z0-9]{6}\/ap_xarray(.*?)\/)"
    print('going into p2p...')
    project_pattern = "(\/proj[a-z0-9]{1}\/[0-9]{5}\/[0-9]{2}[a-z0-9]{6}\/ap(.*?)\/)"

    region_number = ""  # 'proj0'
    project_number = ""  # '12542'
    lineshort_name = ""  # '30305306'
    ap_xarray_label = ""

    has_project_info = False

    def __init__(self, path_or_level: str):
        find_results = re.findall(self.project_pattern,
                                  path_or_level.lower().replace("\\", "/").replace(".", "/") + "/")

        print('find results::::', find_results)
        find_results = find_results[0]
        if len(find_results) > 0:
            parts = find_results[0].strip("/").split("/")  # we take the first find result only
            #print('parts: ', parts)
            assert len(parts) > 3, "Internal error, length of parts does not match"
            self.region_number = parts[0]  # 'proj0'
            self.project_number = parts[1]  # '12542'
            self.lineshort_name = parts[2]  # '30305306'
            self.ap_xarray_label = parts[3]  # would be "AP_xarray_srh5_crawler",
            #self.anomalies_label = parts[4]
            self.has_project_info = True
            return


#
#     '''
#     #project_pattern3 = "(\/proj[a-z0-9]{1}\/[0-9]{5}\/[0-9]{2}[a-z0-9]{6}\/)"
#     #project_pattern4 = "(\/proj[a-z0-9]{1}\/[0-9]{5}\/[0-9]{2}[a-z0-9]{6}\/[a-z0-9_]{7}r[1-9]{1}[a-z]{2}\/)"
#     #project_pattern5 = "(\/proj[a-z0-9]{1}\/[0-9]{5}\/[0-9]{2}[a-z0-9]{6}_r[1-9]{1}[a-z]{2}\/)"
#     project_pattern6 = "(\/proj[a-z0-9]{1}\/[0-9]{5}\/[0-9]{2}[a-z0-9]{6}\/[a-z]{2}_[a-z]{6}\/[a-z]{9}\/[0-9a-z-_]*\/)"
#
#     find_results = re.findall(self.project_pattern6, path_or_level.lower().replace("\\", "/").replace(".", "/") + "/")
#
#     if len(find_results) > 0:
#         parts = find_results[0].strip("/").split("/")  # we take the first find result only
#         assert len(parts) == 6, "Internal error, length of parts does not match"
#         self.region_number = parts[0]  # 'proj0'
#         self.project_number = parts[1]  # '12542'
#         self.lineshort_name = parts[2]  # '30305306'
#         self.ap_xarray_label = parts[3]  # would be "AP_xarray", which is not relevant for this case...
#         self.anomalies_label = parts[4] # 'anomalies'
#         self.single_anomaly_label = parts[5]  # 'plin', or "melo" etc...
#
#         self.has_project_info = True
#         return
#

        # find_results = re.findall(self.project_pattern5, path_or_level.lower().replace("\\", "/").replace(".", "/") + "/")
        # if len(find_results) > 0:
        #     parts = find_results[0].strip("/").split("/")  # we take the first find result only
        #     assert len(parts) == 3, "Internal error, length of parts does not match"
        #     self.region_number = parts[0]  # 'proj0'
        #     self.project_number = parts[1]  # '12542'
        #     self.lineshort_name = parts[2]  # '30305306'
        #     self.has_project_info = True
        #     return

        # find_results = re.findall(self.project_pattern4, path_or_level.lower().replace("\\", "/").replace(".", "/") + "/")
        # if len(find_results)>0:
        #     parts = find_results[0].strip("/").split("/") # we take the first find result only
        #     assert len(parts)==4, "Internal error, length of parts does not match"
        #     self.region_number = parts[0]  # 'proj0'
        #     self.project_number = parts[1] # '12542'
        #     self.lineshort_name = parts[2] # '30305306'
        #     self.run_number = parts[3]
        #     self.has_project_info = True
        #     return
        # find_results = re.findall(self.project_pattern3, path_or_level.lower().replace("\\", "/").replace(".", "/") + "/")
        # if len(find_results)>0:
        #     parts = find_results[0].strip("/").split("/") # we take the first find result only
        #     assert len(parts)==3, "Internal error, length of parts does not match"
        #     self.region_number = parts[0]  # 'proj0'
        #     self.project_number = parts[1] # '12542'
        #     self.lineshort_name = parts[2] # '30305306'
        #     self.has_project_info = True
        #     return





if __name__ == '__main__':        
    # Versuch 1: Ein Pfad mit lustiger Mischung aus Slash und Backslash
    path_to_nc_files = r"//linfile1/groups/EMAT_evaluation_data/CombEvalDataWarehouse\proj0/12542/30305306/AP_xarray/anomalies\lin\14039.nc"
    p = Path2Proj(path_to_nc_files)
    if p.has_project_info:
        print(p)
    else:
        print("Ich habe heute kein Tofu fuer dich, Sonja!")

    # Versuch 2: Ein PDW Level Pfad, ... bitte beachten Sie, dass das Pattern hier zwei mal auftritt
    pdw_level = "EMAT_evaluation_data.CombEvalDataWarehouse.mortadella.proj0.12542.30305306.bli.bla.blo.blubb.gorgonzola.proj7.34567.30Hauweg.anomalies.lin"
    p = Path2Proj(pdw_level)
    if p.has_project_info:
        print(p.to_dict())
    else:
        print("Ich habe heute kein Tofu fuer dich, Sonja!...")

    # Versuch 3: Definitiver Quatsch
    quatsch = "Haha, ... er glaubt ich waere ein Pfad auf ein nc-File, ... bin ich aber gar nicht" 
    p = Path2Proj(quatsch)
    if p.has_project_info:
        print(p.lineshort_name)
    else:
        print("Ich habe heute kein Tofu fuer dich, Sonja!, weil du quatsch erzählt")
    