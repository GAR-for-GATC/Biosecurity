#  This program will take an XML file from a local BLAST search (not internet
# based) and will print the relevent information and return it.

#NOTE: Major bugs have been found in this code.  Rewriting is in progress as of 8/9/13 

#Give the function the file name and the pathway
def local_XML_interpreter(the_file_name, file_pathway): 
    import re

    #   Why are the values not stored in dictionaries?
    # Multiple dictionaries will be needed to store multiple results
    # creating a large number of values stored in an unorganized fashion.
    # An SQLite database simplifies passing information from one function
    # to another without having to deal with multiple dictionaries.

    #   Explanation of the XML interpreting code.
    # 3 values are used to find all the relevent information inside the
    # text file (XML file) created by a local blast search.  The reason
    # why each value was chosen is explained below.
    # 
    #   This program locates values by using the location of specific words
    # that are only generated once in each BLAST result (the words "reference",
    # "Identites" and "Gapped" are used).  An anaogy for how the program
    # searches goes as follows: if you know that the TV is located at the
    # coordinates 0,0 on the coordinate plain and we know that the fridge
    # is 5 units to the left and 3 down, we can find the location of the
    # fridge based on just the relative position of the TV).  Each value in
    # the XML file is located in a similar fashion.
    #   The reason three reference values are needed instead of one is that
    # thre can be a variable number of lines between each value. If there
    # are an unkown number of lines between the fridge and the TV, it is
    # to locate it with certainty.  Each of the key word values used in this
    # program are a set number of rows away from the important values that
    # need to be located.

#  An example notpad file from which the function below locates information.

##BLASTN 2.2.28+
##
##
##Reference: Zheng Zhang, Scott Schwartz, Lukas Wagner, and Webb
##Miller (2000), "A greedy algorithm for aligning DNA sequences", J
##Comput Biol 2000; 7(1-2):203-14.
##
##
##
##Database: Test_database_of_pathogenic_proteins.txt
##           5 sequences; 12,233 total letters
##
##
##
##Query= 
##Length=140
##                                                                      Score     E
##Sequences producing significant alignments:                          (Bits)  Value
##
##  gi|10313991:5538-8665 Ebola virus - Mayinga, Zaire, 1976 strain...   259    1e-072
##
##
##> gi|10313991:5538-8665 Ebola virus - Mayinga, Zaire, 1976 strain 
##Mayinga
##Length=3128
##
## Score =  259 bits (140),  Expect = 1e-072
## Identities = 140/140 (100%), Gaps = 0/140 (0%)
## Strand=Plus/Plus
##
##Query  1     AGGACCCGTCTAGTGGCTACTATTCTACCACAATTAGATATCAGGCTACCGGTTTTGGAA  60
##             ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
##Sbjct  1121  AGGACCCGTCTAGTGGCTACTATTCTACCACAATTAGATATCAGGCTACCGGTTTTGGAA  1180
##
##Query  61    CCAATGAGACAGAGTACTTGTTCGAGGTTGACAATTTGACCTACGTCCAACTTGAATCAA  120
##             ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
##Sbjct  1181  CCAATGAGACAGAGTACTTGTTCGAGGTTGACAATTTGACCTACGTCCAACTTGAATCAA  1240
##
##Query  121   GATTCACACCACAGTTTCTG  140
##             ||||||||||||||||||||
##Sbjct  1241  GATTCACACCACAGTTTCTG  1260
##
##
##
##Lambda      K        H
##    1.33    0.621     1.12 
##
##Gapped
##Lambda      K        H
##    1.28    0.460    0.850 
##
##Effective search space used: 1545336
##
##
##  Database: Test_database_of_pathogenic_proteins.txt
##    Posted date:  Jul 15, 2013  1:03 PM
##  Number of letters in database: 12,233
##  Number of sequences in database:  5
##
##
##
##Matrix: blastn matrix 1 -2
##Gap Penalties: Existence: 0, Extension: 2.5

#~~~Creates database 
    db_name = "temp_db"
    db_path = "C:\Users\Evan\Desktop"
    SQL_db_create(db_name, db_path)

#~~~Create a table inside the database to store values
    dictionary_of_columns = {"the_reference":"TEXT", "sequence_fasta_name":"TEXT", "score_value":"TEXT", "expect_value":"TEXT", "identities_value":"TEXT", "gaps_value":"TEXT", "strand_value":"TEXT", "subject_lines":"TEXT", "dash_lines":"TEXT", "query_lines":"TEXT", "lambda_value":"TEXT", "lambda_k_value":"TEXT", "lambda_h_value":"TEXT", "gapped_lambda_value":"TEXT", "gapped_k_value":"TEXT", "gapped_h_value":"TEXT", "matrix_value":"TEXT", "existence_gap_penalty":"TEXT", "extension_gap_penalty":"TEXT"}
    table_name = "temp_table"
    SQL_create_table(table_name, db_name, db_path, dictionary_of_columns)


    


    list_of_inportant_parameters = ["Reference", "Identities", "Gapped"]
##-------------------------------------------------------------
##   This short code will go through the file given to the function and will
## search for the parameters in the list_of_inportant_parameters variable.
    for parameters in list_of_inportant_parameters:
        patterns = [r'\b%s\b' % re.escape(parameters.strip())]
        there = re.compile('|'.join(patterns))
        
        with open(file_pathway + "\\" + the_file_name + ".txt") as f:
        # i is a counter
        # s is the actuall line in new_file
            #~~~SQL id counter~~~ Unique primary id's are not created automaticly
            #   by python's SQLite3.  Instead, they each need to be inserted manually.  In this
            #   program, they are inserted when a new row is created (the INSERT command).
            #   The counter below is used to create unique id numbers that are inserted
            #   when the FASTA_lit_Reference names are input into the SQL database.
            unique_id_counter = 1

            for i, s in enumerate(f):
                
                if there.search(s):
                    #print("Line %s: %r" % (i, s))
##-------------------------------------------------------------
                    if parameters == "Reference":
                        #___FASTA_lit_Reference___#
                        the_reference = grab_lines(the_file_name, file_pathway, i, 3, 0, "down")
                        delete_this = "Reference: "
                        # The string to be deleted needs to be in regular explression format
                        finished_ref = delete_the_thing_in_the_string("\s?" + delete_this + "\s?", the_reference)

                        id_and_ref_list = [unique_id_counter, finished_ref]
                        id_and_ref_columns = ["id", "the_reference"]
                        SQL_INSERT_row(db_name, db_path, table_name, id_and_ref_list, id_and_ref_columns)
                        unique_id_counter = unique_id_counter + 1


                    elif parameters == "Identities":
                        
                        #___sequence_fasta_name___#                         
                        the_sequence_name = grab_lines(the_file_name, file_pathway, i, 1, 5, "up")

                        column_name = "sequence_fasta_name"
                        id_number = str(unique_id_counter)
                        new_value = the_sequence_name
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                        

                        #___score_value___# -This is one line up from the identities parameter
                        the_score_value = grab_lines(the_file_name, file_pathway, i, 1, 1, "up")
                        front_deleted_score_value = delete_the_thing_in_the_string("\sScore\s=(\s{2})", the_score_value)
                        final_score_value = delete_the_thing_in_the_string(",\s\sExpect\s=\s(\d+)e(\+?\-?)(\d+)", front_deleted_score_value)
                        

                        column_name = "score_value"
                        id_number = str(unique_id_counter)
                        new_value = final_score_value
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                        

                        #___expect_value___# One line up from identities parameter
                        the_expect_value_line = grab_lines(the_file_name, file_pathway, i, 1, 1, "up")
                        final_expect_value = delete_the_thing_in_the_string("\s(\w+)\s=\s\s(\d+)\s(\w+)\s.(\d+).,\s\s(\w+)\s=\s", the_expect_value_line)

                        column_name = "expect_value"
                        id_number = str(unique_id_counter)
                        new_value = final_expect_value
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                        

                        #___identities_value___#
                        the_identites_value_line = grab_lines(the_file_name, file_pathway, i, 1, 0, "up")
                        delete_the_front_of_the_line = delete_the_thing_in_the_string("\sIdentities\s=\s", the_identites_value_line)
                        finished_identites_value = delete_the_thing_in_the_string(",\s(\w+)\s=\s(\d+).(\d+)\s.(\d+)..", delete_the_front_of_the_line)

                        column_name = "identities_value"
                        id_number = str(unique_id_counter)
                        new_value = finished_identites_value
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                        
                        #___gaps_value___# -Same line as the identites value
                        The_gaps_value_line = grab_lines(the_file_name, file_pathway, i, 1, 0, "up")
                        finished_gaped_value = delete_the_thing_in_the_string("\s(\w+)\s=\s(\d+).(\d+)\s.(\d+)...\s(\w+)\s=\s", The_gaps_value_line)
                        
                        column_name = "gaps_value"
                        id_number = str(unique_id_counter)
                        new_value = finished_gaped_value
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                        

                        #___strand_value___# -one line down from the identities value
                        the_strand_value_line = grab_lines(the_file_name, file_pathway, i, 1, 1, "down")
                        finished_strand_value = delete_the_thing_in_the_string("\s(\w+)=", the_strand_value_line)
                        
                        column_name = "strand_value"
                        id_number = str(unique_id_counter)
                        new_value = finished_strand_value
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                        

                        #___subject_and_query_lines___#############################################################
                        #find the number of sbjct lines close by.
                        #If there is an "sbjct" line, then grab the sbjct line and the 2 lines above it.

                        #loops through the lines after the first 3 lines grabbed
                        the_sbjct_line = grab_lines(the_file_name, file_pathway, i, 1, 5, "down")# 5 lines down from the identites line
                        
                        the_dash_line = grab_lines(the_file_name, file_pathway, i, 1, 4, "down")
                        
                        the_query_line = grab_lines(the_file_name, file_pathway, i, 1, 3, "down")
                        

                        ###############Add the qurey line, dash line, and sbjct line to the SQLite3 database in different columns

                        #______________# The next part of the code will loop through the lines immediatley below the lines just added to the
                        #               database and will look for the word 'Sbjct'.  If it does find "Sbjct", it will add 3 lines to the database
                        #               (the sbjct line, a line with dashes and a line with the query).  If not, then the code will add nothing. 
                        does_this_have_sbjct_in_it = grab_lines(the_file_name, file_pathway, i, 1, 9, "down")
                        

                        counter = 4
                        finder = re.findall("Sbjct", does_this_have_sbjct_in_it)
                     
                        
                        while finder != "no_sbjct" :
                            
                            the_sbjct_line = the_sbjct_line + does_this_have_sbjct_in_it
                            
                            the_dash_line2 = grab_lines(the_file_name, file_pathway, i, 1, (4 + counter), "down")
                            the_dash_line = the_dash_line + the_dash_line2
                            
                            the_query_line2 = grab_lines(the_file_name, file_pathway, i, 1, (3 + counter), "down")
                            the_query_line = the_query_line + the_query_line2
                             

                            #############put the prior sbjct line, dash line and query line in database

                            # don't add this one yet to the db, it needs to be checked to see if it has "Sbjct" in it.
                            does_this_have_sbjct_in_it = grab_lines(the_file_name, file_pathway, i, 1, (9 + counter), "down")
                            
                            
                            new_finder = re.findall("Sbjct", does_this_have_sbjct_in_it)
                            counter = counter + 4

                            
                            if new_finder == []:
                                finder = "no_sbjct"

                        #Adding stuff to the database
                        column_name = "subject_lines"
                        id_number = str(unique_id_counter)
                        new_value = the_sbjct_line
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)

                        column_name = "dash_lines"
                        id_number = str(unique_id_counter)
                        new_value = the_dash_line
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)

                        column_name = "query_lines"
                        id_number = str(unique_id_counter)
                        new_value = the_query_line
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)


                        unique_id_counter = unique_id_counter + 1
                        ###############################################################################

                        
                    elif parameters == "Gapped": #if the parameter is Gapped

                        #___lambda_value___# -this one is wierd, no markers besides numbers on that line.  Grabbed 2 lines to delete the right numbers.
                        the_lambda_value_lines = grab_lines(the_file_name, file_pathway, i, 2, 3, "up")
                        delete_first_part = delete_the_thing_in_the_string("(\w+)(\s+)\w(\s+)\w(\s+)", the_lambda_value_lines)
                        finished_lambda_value = delete_the_thing_in_the_string("\s+(.+)", delete_first_part)
                        
                        column_name = "lambda_value"
                        id_number = str(unique_id_counter)
                        new_value = finished_lambda_value
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                        

                        #___lambda_k_value___#
                        the_lambda_k_value_lines = grab_lines(the_file_name, file_pathway, i, 2, 3, "up")
                        delete_the_first_part = delete_the_thing_in_the_string("(\w+)(\s+)\w(\s+)\w(\s+)\d+.(\d+)(\s+)", the_lambda_k_value_lines)
                        finished_k_value = delete_the_thing_in_the_string("(\s+)(\d+).(\d+)", delete_the_first_part )

                        column_name = "lambda_k_value"
                        id_number = str(unique_id_counter)
                        new_value = finished_k_value
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                        

                        #___lambda_h_value___#
                        the_lambda_h_value_lines = grab_lines(the_file_name, file_pathway, i, 2, 3, "up")
                        lambda_h_value = delete_the_thing_in_the_string("(\w+)(\s+)\w(\s+)\w(\s+)\d+.(\d+)(\s+)(\d+).(\d+)(\s+)", the_lambda_h_value_lines)

                        column_name = "lambda_h_value"
                        id_number = str(unique_id_counter)
                        new_value = lambda_h_value
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                        

                        #___gapped_lambda_value___# -Grabbing the two lines below gapped.  Using the exact same code as the regular lambda values otherwise.
                        the_gapped_lambda_value_lines = grab_lines(the_file_name, file_pathway, i, 2, 1, "down")
                        delete_first_part_gapped = delete_the_thing_in_the_string("(\w+)(\s+)\w(\s+)\w(\s+)", the_gapped_lambda_value_lines)
                        finished_gapped_lambda_value = delete_the_thing_in_the_string("\s+(.+)", delete_first_part_gapped)

                        column_name = "gapped_lambda_value"
                        id_number = str(unique_id_counter)
                        new_value = finished_gapped_lambda_value
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                        

                        #___gapped_k_value___#
                        the_gapped_k_value_lines = grab_lines(the_file_name, file_pathway, i, 2, 1, "down")
                        delete_the_first_part_gapped_k = delete_the_thing_in_the_string("(\w+)(\s+)\w(\s+)\w(\s+)\d+.(\d+)(\s+)", the_gapped_k_value_lines)
                        finished_gapped_k_value = delete_the_thing_in_the_string("(\s+)(\d+).(\d+)", delete_the_first_part_gapped_k )

                        column_name = "gapped_k_value"
                        id_number = str(unique_id_counter)
                        new_value = finished_gapped_k_value
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                        

                        #___gapped_h_value___#
                        the_gapped_h_value_lines = grab_lines(the_file_name, file_pathway, i, 2, 1, "down")
                        gapped_h_value = delete_the_thing_in_the_string("(\w+)(\s+)\w(\s+)\w(\s+)\d+.(\d+)(\s+)(\d+).(\d+)(\s+)", the_gapped_h_value_lines)

                        column_name = "gapped_h_value"
                        id_number = str(unique_id_counter)
                        new_value = gapped_h_value
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                        

                        
                        #___matrix_value___# 14 spaces down from te word "Gapped"
                        the_matrix_value_line = grab_lines(the_file_name, file_pathway, i, 1, 14, "down")
                        matrix_value = delete_the_thing_in_the_string("Matrix:\s", the_matrix_value_line)

                        column_name = "matrix_value"
                        id_number = str(unique_id_counter)
                        new_value = matrix_value
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                        

                        #___existence_gap_penalty___# 15 lines down
                        the_line = grab_lines(the_file_name, file_pathway, i, 1, 15, "down")
                        first_part_removed_really_tired = delete_the_thing_in_the_string("Gap\sPenalties.\sExistence.\s", the_line)
                        existence_gap_penalty = delete_the_thing_in_the_string(',\sExtension.\s(\d+).(\d+)', first_part_removed_really_tired)

                        column_name = "existence_gap_penalty"
                        id_number = str(unique_id_counter)
                        new_value = existence_gap_penalty
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                        
                        
                        #___extension_gap_penalty___# 15 lines down
                        omfg_this_is_boring = grab_lines(the_file_name, file_pathway, i, 1, 15, "down")
                        i_need_sleep = delete_the_thing_in_the_string("Gap\sPenalties.\sExistence.\s(\d+),\sExtension.\s", omfg_this_is_boring)
                        
                        column_name = "extension_gap_penalty"
                        id_number = str(unique_id_counter)
                        new_value = i_need_sleep
                        SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                        unique_id_counter = unique_id_counter + 1
                        

                        
    return    

def grab_lines(the_file_name, file_pathway, the_reference_line_number, number_of_lines_to_grab, how_many_lines_from_reference, read_up_or_down):
    #   This function will return a number of lines a set distance away from
    # a reference line.
    #   read_up_or_down indicates whether the function will grab lines up or
    # down from the reference line.  This script will always take lines from
    # below the line first grabbed when retriving multiple lines.

    with open(file_pathway + "\\" + the_file_name + ".txt", 'r') as file:
        data = file.readlines()
        if read_up_or_down == "up":
            string_for_lines = ""
            counter = 0
            while number_of_lines_to_grab != 0:
                string_for_lines = string_for_lines + data[(the_reference_line_number + counter) - how_many_lines_from_reference ]
                counter = counter + 1
                number_of_lines_to_grab = number_of_lines_to_grab - 1
            return string_for_lines

        elif read_up_or_down == "down":
            string_for_lines = ""
            counter = 0
            while number_of_lines_to_grab != 0:
                string_for_lines = string_for_lines + data[(the_reference_line_number + counter) + how_many_lines_from_reference ]
                counter = counter + 1
                number_of_lines_to_grab = number_of_lines_to_grab - 1
            return string_for_lines
            
    
# This deletes something from a string. ***The thing to delete needs to be in regular expression format!!!***
def delete_the_thing_in_the_string(the_word_or_phrase_to_delete, the_string_to_delete_from):
    import re
    stuff_to_find = re.compile(the_word_or_phrase_to_delete)
    find = re.findall(stuff_to_find, the_string_to_delete_from)
    split_find = stuff_to_find.split(the_string_to_delete_from)
    new_string = stuff_to_find.sub("",the_string_to_delete_from)
    
    return new_string

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SQLite 3 Code~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def SQL_db_create(db_name, db_path):
    import sqlite3
    new_db = sqlite3.connect(db_path + "\\" + db_name + ".db")
    new_db.close()
    return

#dictionary should be in {"column_name":"TEXT", etc.} format
def SQL_create_table(table_name, db_name, db_path, dictionary_of_columns):
    import sqlite3
    open_db = sqlite3.connect(db_path + "\\" + db_name + ".db")

    # Takes the dictionary, turns it to lists, 
    list_of_column_names = []
    list_of_column_data_types = []
    for i in dictionary_of_columns:
        list_of_column_names.append(i)
        list_of_column_data_types.append(dictionary_of_columns[i])

    # Build the string to insert into the CREATE TABLE commmand
    put_in_table = "CREATE TABLE " + table_name + " (id TEXT PRIMARY KEY, "
    for i in range(len(dictionary_of_columns)):
        if i == (len(dictionary_of_columns) - 1):
            put_in_table = put_in_table + str(list_of_column_names[i]) + " " + str(list_of_column_data_types[i]) + ");"
        else:
            put_in_table = put_in_table + str(list_of_column_names[i]) + " " + str(list_of_column_data_types[i]) + ", "
            
    print put_in_table
    open_db.execute(put_in_table)
    open_db.close()
    return
    
#   Inserts one row to a table.  list_to_add and columns_to_add_to are both lists
# with the same number of items in them.
def SQL_INSERT_row(db_name, db_path, table_name, list_to_add, columns_to_add_to):
    import sqlite3
    open_db = sqlite3.connect(db_path + "\\" + db_name + ".db")

    #Building the string to insert into the INSERT ROW command
    create_string = "INSERT INTO " + table_name + " ("
    for i in range(len(list_to_add)):
        if i == (len(columns_to_add_to) - 1):
            create_string = create_string + str(columns_to_add_to[i]) + ") "
        else:
            create_string = create_string + str(columns_to_add_to[i]) + ","
    create_string = create_string + "VALUES ("
    for i in range(len(list_to_add)):
        if i == (len(list_to_add) - 1):
            create_string = create_string + "\'" + str(list_to_add[i])+ "\'"  + ")"
        else:
            create_string = create_string + "\'" + str(list_to_add[i]) + "\'" + ", "
    print create_string

    open_db.execute(create_string)
    open_db.commit()
    
    open_db.close()

    return

# This selects all rows in a table
def SQL_SELECT_rows(db_name, db_path, table_name):
    import sqlite3
    open_db = sqlite3.connect(db_path + "\\" + db_name + ".db")

    everything = open_db.execute("SELECT * FROM " + table_name)
    for row in everything:
        print row
           
    return

#This changes one value in one row in a table inside a database
def SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number):
    import sqlite3
    open_db = sqlite3.connect(db_path + "\\" + db_name + ".db")

    usable_string = "  UPDATE " + table_name + " SET " + column_name + ' = \'' + new_value + '\' WHERE id = ' + str(id_number) + " "
    print usable_string

    open_db.execute(usable_string)
    open_db.commit()
    
    open_db.close()
    
    return
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def main():
    the_file_name = "new_file"
    file_pathway = "C:/Users/Evan/Desktop"

    local_XML_interpreter(the_file_name, file_pathway)

    db_name = "temp_db"
    db_path = "C:/Users/Evan/Desktop"
    table_name = "temp_table"
    SQL_SELECT_rows(db_name, db_path, table_name)


main()





    
