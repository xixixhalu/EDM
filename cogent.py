import sys, os, argparse
from werkzeug.utils import secure_filename
import uuid
from shutil import copyfile

from uml_parser.parse_dm_file import Analyzer
from code_generator import generate_code
from utilities.config_util import ConfigUtil
from utilities.file_op import fileOps
from database_manager.dbOps import dbOps


def cogent(inputfile, output_dir):

    filename = secure_filename(os.path.basename(inputfile))
    filename_str = filename.split(".")[0]

    input_dir = inputfile
    # output_dir = os.path.join(outputdir)

    # generate a uuid to store different versions of uploads
    #file_id = str(uuid.uuid4())
    # output_dir = output_dir + '/' + file_id

    fileOps.mkdir_p(output_dir)
    copyfile(input_dir, output_dir + '/' + filename)

    # Parse XML and generate JSON
    ana = Analyzer()
    ana.DM_File_Analyze(output_dir, {'DM_Input_type': "Simple_XML"}, filename_str)
    
    generate_code.generate_all(filename_str, output_dir)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog=os.path.basename(__file__), 
                                    epilog="The rest of values can be set in config.properties.")
    parser.add_argument('-i', metavar='<inputfile>', type=str, required=True,
                    help='path of the input file')
    parser.add_argument('-o', metavar='<outputfile>', type=str, 
                    default=ConfigUtil().get('Output', 'output_path'),
                    help='the root dir of output. (default: see config.properties)')
    args = vars(parser.parse_args())

    inputfile = args.get("i")
    outputfile = args.get("o")
    username = args.get("u")

    print 'Input is ' + inputfile
    print 'Output is ' + outputfile

    cogent(inputfile, outputfile)