#---Notes for version 2.1---#
#   Version 2.1 includes an if statement that will end the program if
# if it runs into the words "***** No hits found *****", which indicate that
# no results appear in the xml file.

#---Notes for version 2---#
#   This is an improved version of the XML parser.
# Changes to the original XML parser are:
#  1) The elimination of the reference value (it is worthless)
#  2) Placing different BLAST searches in different tables while
#    placing the different BLAST results in different rows inside each
#    table.
#  3) Checking for different BLAST results

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

    #   This program locates values by using the location of specific words
    # that are only generated once in each BLAST result (the words
    # "Sequences producing significant alignments:", "Identites" and "Gapped"
    # are used).
    # An anaogy for how the program searches goes as follows: if you know
    # that the TV is located at the coordinates 0,0 on the coordinate plain
    # and we know that the fridge is 5 units to the left and 3 down, we can
    # find the location of the fridge based on just the relative position of
    # the TV).  Each value in the XML file is located in a similar fashion.
    #   The reason three reference values are needed instead of one is that
    # thre can be a variable number of lines between each value. If there
    # are an unkown number of lines between the fridge and the TV, it is
    # to locate it with certainty.  Each of the key word values used in this
    # program are a set number of rows away from the important values that
    # need to be located.

    ####Example fasta files are provided at the end of the program.####

    #~~~Creates database 
    db_name = "temp_db"
    db_path = file_pathway #"C:\Users\Evan\Desktop" 
    SQL_db_create(db_name, db_path)


    list_to_find_BLAST_searches = ["2.2.28+"]
    number_of_BLAST_searches_counter = 0
    name_of_BLAST_searches_tables = []
    #   This counter below counts the line number where the
    # word "2.2.28+" occurs
    blast_search_line_counter = []
##   This code will go through the file given to the function and will
## search for the number of instances of the word "2.2.28+" with any number
## of letters in frnt of it.
    for parameters in list_to_find_BLAST_searches:
        patterns = [r'\b%s\b' % parameters]
        there = re.compile('|'.join(patterns))
        with open(file_pathway + "\\" + the_file_name + ".txt") as f:
       
            table_counter = 1

            # i is a counter for the line number
            # s is a line in the file 
            for i, s in enumerate(f):
                # if the line contains "2.2.28+"
                if there.search(s):
                    blast_search_line_counter.append(i)
                    number_of_BLAST_searches_counter = number_of_BLAST_searches_counter + 1
                    name_of_BLAST_searches_tables.append("table_%d" %table_counter)
                    table_counter = table_counter + 1
    #print blast_search_line_counter    


#creates a table with the number of table names inside it
    master_name = "master_table"
    master_dic_of_columns = {"table_name":"TEXT"}
    SQL_create_table(master_name, db_name, db_path, master_dic_of_columns)
    for purple in range(number_of_BLAST_searches_counter):
        #print "meh: ", purple
        master_list_to_add =  [ str(purple+500000), name_of_BLAST_searches_tables[purple]]
        #print master_list_to_add
        master_columns_to_add_to = ["id", "table_name"]
        SQL_INSERT_row(db_name, db_path, master_name, master_list_to_add, master_columns_to_add_to)

    # Creates temporary text files containing each BLAST search
    starting_line_list = blast_search_line_counter
    ending_line_list = find_instance_line_numbers(the_file_name, file_pathway, "Gapped")
    for green in name_of_BLAST_searches_tables:

        #Creates a table for each BLAST search
        dictionary_of_columns = {"database_details":"TEXT", "query_length":"TEXT", "sequence_length":"TEXT", "sequence_fasta_name":"TEXT", "score_value":"TEXT", "expect_value":"TEXT", "identities_value":"TEXT", "gaps_value":"TEXT", "strand_value":"TEXT", "subject_lines":"TEXT", "dash_lines":"TEXT", "query_lines":"TEXT", "lambda_value":"TEXT", "lambda_k_value":"TEXT", "lambda_h_value":"TEXT", "gapped_lambda_value":"TEXT", "gapped_k_value":"TEXT", "gapped_h_value":"TEXT", "matrix_value":"TEXT", "existence_gap_penalty":"TEXT", "extension_gap_penalty":"TEXT"}
        table_name = green
        #db name and path are already defined
        SQL_create_table(table_name, db_name, db_path, dictionary_of_columns)

        with open(file_pathway + "\\" + green + ".txt", 'w') as file:
            #grab_lines(the_file_name, file_pathway, the_reference_line_number, number_of_lines_to_grab, how_many_lines_from_reference, read_up_or_down)
            one_BLAST_search = grab_lines(the_file_name, file_pathway, starting_line_list[name_of_BLAST_searches_tables.index(green)] , ((ending_line_list[name_of_BLAST_searches_tables.index(green)]) - (starting_line_list[name_of_BLAST_searches_tables.index(green)])) + 16, 0, "down")                        
            file.write(one_BLAST_search)
            #print "wrote: ", green
        

        my_list_of_parameters = ["No hits found", "Identities", "Gapped"]
        unique_id_counter = 1

        for parameters in my_list_of_parameters:
            patterns = [r'\b%s\b' % re.escape(parameters.strip())]
            there = re.compile('|'.join(patterns))
        
            with open(file_pathway + "\\" + green + ".txt") as f:
                for i, s in enumerate(f):
                    # i is the line number
                    # s is the line from the file                
                    if there.search(s):
                        #print("Line %s: %r" % (i, s))
                        
                        if parameters == "No hits found":
                            print "-----------------------------------------------"
                            print '\n'
                            print "No hits found."
                            print "\n"
                            print "\n"
                            return

                        elif parameters == "Identities":

                            #___sequence_length___#
                            the_sequence_length = grab_lines(green , file_pathway, i, 1, 3, "up")
                            #print "this is ref line: ", i
                            #print "grabbed line: ", the_query_length
                            kiiro = delete_the_thing_in_the_string("Length=", the_sequence_length)
                            finished_length = delete_the_thing_in_the_string("(\n)", kiiro)
                                
                            id_and_ref_list = [unique_id_counter, finished_length]
                            id_and_len_columns = ["id", "sequence_length"]
                            #SQL_INSERT_row(db_name, db_path, table_name, id_and_ref_list, id_and_len_columns)
                            #print green, "length = ", finished_length 
                            SQL_INSERT_row(db_name, db_path, green, id_and_ref_list, id_and_len_columns)


                            

                            
                            #___sequence_fasta_name___#                         
                            shiroi = grab_lines(green, file_pathway, i, 1, 5, "up")
                            the_sequence_name = delete_the_thing_in_the_string("(\n)", shiroi)

                            column_name = "sequence_fasta_name"
                            id_number = str(unique_id_counter)
                            new_value = the_sequence_name
                            #print green, "the_sequence_name = ", the_sequence_name
                            SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                            

                            #___score_value___# -This is one line up from the identities parameter
                            the_score_value = grab_lines(green, file_pathway, i, 1, 1, "up")
                            front_deleted_score_value = delete_the_thing_in_the_string("\sScore\s=(\s\s?)", the_score_value)
                            aoi = delete_the_thing_in_the_string(",\s\sExpect\s=\s(\d+)(\.?\d?\d?)e(\+?\-?)(\d+)(\.?\d?\d?)", front_deleted_score_value)
                            final_score_value = delete_the_thing_in_the_string("(\n)", aoi)
                            #print "the_score_value: ", the_score_value
                            #print "final_score_value: ", final_score_value

                            column_name = "score_value"
                            id_number = str(unique_id_counter)
                            new_value = final_score_value
                            SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                            

                            #___expect_value___# One line up from identities parameter
                            the_expect_value_line = grab_lines(green, file_pathway, i, 1, 1, "up")
                            #final_expect_value = delete_the_thing_in_the_string("\s(\w+)\s=\s\s(\d+)(\.?)(\d?\d?)\s(\w+)\s.(\d+).,\s\s(\w+)\s=\s", the_expect_value_line)
                            kuroi = delete_the_thing_in_the_string("\s?(\w+)\s(=)\s\s?\d+(\.?\d?\d?)\s\w+\s.\d+(\.?\d?\d?)..\s\sExpect\s=\s", the_expect_value_line)
                            final_expect_value = delete_the_thing_in_the_string("(\n)", kuroi)
                            #print "the_expect_value_line: ", the_expect_value_line
                            #print "final_expect_value: ", final_expect_value
                            column_name = "expect_value"
                            id_number = str(unique_id_counter)
                            new_value = final_expect_value
                            SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)


                            #___identities_value___#
                            the_identites_value_line = grab_lines(green, file_pathway, i, 1, 0, "up")
                            delete_the_front_of_the_line = delete_the_thing_in_the_string("\sIdentities\s=\s", the_identites_value_line)
                            pinku = delete_the_thing_in_the_string(",\s(\w+)\s=\s(\d+)(\.?\d?\d?).(\d+)(\.?\d?\d?)\s.(\d+)(\.?\d?\d?)..", delete_the_front_of_the_line)
                            finished_identites_value = delete_the_thing_in_the_string("(\n)", pinku)
                            
                            column_name = "identities_value"
                            id_number = str(unique_id_counter)
                            new_value = finished_identites_value
                            SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)

                            #___gaps_value___# -Same line as the identites value
                            The_gaps_value_line = grab_lines(green, file_pathway, i, 1, 0, "up")
                            midori = delete_the_thing_in_the_string("\s(\w+)\s=\s(\d+)(\.?\d?\d?).(\d+)(\.?\d?\d?)\s.(\d+)(\.?\d?\d?)...\s(\w+)\s=\s", The_gaps_value_line)
                            finished_gaped_value = delete_the_thing_in_the_string("(\n)", midori)
                            
                            column_name = "gaps_value"
                            id_number = str(unique_id_counter)
                            new_value = finished_gaped_value
                            SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)

                            #___strand_value___# -one line down from the identities value
                            the_strand_value_line = grab_lines(green, file_pathway, i, 1, 1, "down")
                            blargh = delete_the_thing_in_the_string("\s(\w+)=", the_strand_value_line)
                            finished_strand_value = delete_the_thing_in_the_string("(\n)", blargh)
                            
                            column_name = "strand_value"
                            id_number = str(unique_id_counter)
                            new_value = finished_strand_value
                            SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                            
                            #___subject_and_query_lines___#############################################################
                            #find the number of sbjct lines close by.
                            #If there is an "sbjct" line, then grab the sbjct line and the 2 lines above it.

                            #loops through the lines after the first 3 lines grabbed
                            the_sbjct_line = grab_lines(green, file_pathway, i, 1, 5, "down")# 5 lines down from the identites line
                            
                            the_dash_line = grab_lines(green, file_pathway, i, 1, 4, "down")
                            
                            the_query_line = grab_lines(green, file_pathway, i, 1, 3, "down")
                            

                            ###############Add the qurey line, dash line, and sbjct line to the SQLite3 database in different columns

                            #______________# The next part of the code will loop through the lines immediatley below the lines just added to the
                            #               database and will look for the word 'Sbjct'.  If it does find "Sbjct", it will add 3 lines to the database
                            #               (the sbjct line, a line with dashes and a line with the query).  If not, then the code will add nothing. 
                            does_this_have_sbjct_in_it = grab_lines(green, file_pathway, i, 1, 9, "down")
                            

                            counter = 4
                            finder = re.findall("Sbjct", does_this_have_sbjct_in_it)
                         
                            
                            while finder != "no_sbjct" :
                                
                                the_sbjct_line = the_sbjct_line + does_this_have_sbjct_in_it
                                
                                the_dash_line2 = grab_lines(green, file_pathway, i, 1, (4 + counter), "down")
                                the_dash_line = the_dash_line + the_dash_line2
                                
                                the_query_line2 = grab_lines(green, file_pathway, i, 1, (3 + counter), "down")
                                the_query_line = the_query_line + the_query_line2
                                 

                                #############put the prior sbjct line, dash line and query line in database

                                # don't add this one yet to the db, it needs to be checked to see if it has "Sbjct" in it.
                                does_this_have_sbjct_in_it = grab_lines(green, file_pathway, i, 1, (9 + counter), "down")
                                
                                
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
                            the_lambda_value_lines = grab_lines(green, file_pathway, i, 2, 3, "up")
                            delete_first_part = delete_the_thing_in_the_string("(\w+)(\s+)\w(\s+)\w(\s+)", the_lambda_value_lines)
                            delete_second_part = delete_the_thing_in_the_string("\s+(.+)", delete_first_part)
                            finished_lambda_value = delete_the_thing_in_the_string("(\n)", delete_second_part)

                            #print "purple"
                            #print "the_lambda_value_lines: ", the_lambda_value_lines
                            #print "finished_lambda_value: ", finished_lambda_value
                            #print "unique_id_counter: ", unique_id_counter
                            #print "table name: ", green
                            
                            columns_to_add_to = ["id", "lambda_value"]
                            id_number = str(unique_id_counter)
                            list_to_add = [id_number, finished_lambda_value]
                            new_value = finished_lambda_value
                            SQL_INSERT_row(db_name, db_path, green, list_to_add, columns_to_add_to)
                            #SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                            #unique_id_counter = unique_id_counter + 1
                         

                            #___query_length___#
                            murasaki = grab_lines(green, file_pathway, 1, 1, 14, "down")
                            no_newline = delete_the_thing_in_the_string("(\n)", murasaki)
                            the_query_length = delete_the_thing_in_the_string("Length=", no_newline)

                            column_name = "query_length"
                            id_number = str(unique_id_counter)
                            new_value = the_query_length
                            #print green, "the_query_length = ", the_query_length
                            SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)

                            #___database_details___#
                            mazenta = grab_lines(green, file_pathway, 1, 2, 8, "down")
                            no_newlines = delete_the_thing_in_the_string("(\n)", mazenta)
                            yuzu = delete_the_thing_in_the_string("(\.txt)(\s{10})", mazenta)
                            database_details = delete_the_thing_in_the_string("Database:", yuzu)

                            column_name = "database_details"
                            id_number = str(unique_id_counter)
                            new_value = database_details
                            #print green, "database_details = ", database_details
                            SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                                                   
                            

                            #___lambda_k_value___#
                            the_lambda_k_value_lines = grab_lines(green, file_pathway, i, 2, 3, "up")
                            delete_the_first_part = delete_the_thing_in_the_string("(\w+)(\s+)\w(\s+)\w(\s+)\d+.(\d+)(\s+)", the_lambda_k_value_lines)
                            second_part_delete = delete_the_thing_in_the_string("(\n)", delete_the_first_part)
                            finished_k_value = delete_the_thing_in_the_string("(\s+)(\d+).(\d+)", second_part_delete )

                            #print "finished_k_value", finished_k_value
                            column_name = "lambda_k_value"
                            id_number = str(unique_id_counter)
                            new_value = finished_k_value
                            SQL_UPDATE_row(db_name, db_path, green, column_name ,new_value, id_number)

                            #___lambda_h_value___#
                            the_lambda_h_value_lines = grab_lines(green, file_pathway, i, 2, 3, "up")
                            number_two = delete_the_thing_in_the_string("(\w+)(\s+)\w(\s+)\w(\s+)\d+.(\d+)(\s+)(\d+).(\d+)(\s+)", the_lambda_h_value_lines)
                            lambda_h_value= delete_the_thing_in_the_string("(\n)", number_two)

                            column_name = "lambda_h_value"
                            id_number = str(unique_id_counter)
                            new_value = lambda_h_value
                            SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                        

                            #___gapped_lambda_value___# -Grabbing the two lines below gapped.  Using the exact same code as the regular lambda values otherwise.
                            the_gapped_lambda_value_lines = grab_lines(green, file_pathway, i, 2, 1, "down")
                            delete_first_part_gapped = delete_the_thing_in_the_string("(\w+)(\s+)\w(\s+)\w(\s+)", the_gapped_lambda_value_lines)
                            second_part_delete_gapped = delete_the_thing_in_the_string("\s+(.+)", delete_first_part_gapped)
                            finished_gapped_lambda_value = delete_the_thing_in_the_string("(\n)", second_part_delete_gapped)
                            
                            column_name = "gapped_lambda_value"
                            id_number = str(unique_id_counter)
                            new_value = finished_gapped_lambda_value
                            SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)

                            #___gapped_k_value___#
                            the_gapped_k_value_lines = grab_lines(green, file_pathway, i, 2, 1, "down")
                            delete_the_first_part_gapped_k = delete_the_thing_in_the_string("(\w+)(\s+)\w(\s+)\w(\s+)\d+.(\d+)(\s+)", the_gapped_k_value_lines)
                            delete_two = delete_the_thing_in_the_string("(\s+)(\d+).(\d+)", delete_the_first_part_gapped_k )
                            finished_gapped_k_value = delete_the_thing_in_the_string("(\n)", delete_two)
                            
                            column_name = "gapped_k_value"
                            id_number = str(unique_id_counter)
                            new_value = finished_gapped_k_value
                            SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                            

                            #___gapped_h_value___#
                            the_gapped_h_value_lines = grab_lines(green, file_pathway, i, 2, 1, "down")
                            delete_thiss = delete_the_thing_in_the_string("(\w+)(\s+)\w(\s+)\w(\s+)\d+.(\d+)(\s+)(\d+).(\d+)(\s+)", the_gapped_h_value_lines)
                            gapped_h_value = delete_the_thing_in_the_string("(\n)", delete_thiss)

                            column_name = "gapped_h_value"
                            id_number = str(unique_id_counter)
                            new_value = gapped_h_value
                            SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)

                            #___matrix_value___# 14 spaces down from te word "Gapped"
                            the_matrix_value_line = grab_lines(green, file_pathway, i, 1, 14, "down")
                            matrix_value_with_newline = delete_the_thing_in_the_string("Matrix:\s", the_matrix_value_line)
                            matrix_value = delete_the_thing_in_the_string("(\n)", matrix_value_with_newline)

                            column_name = "matrix_value"
                            id_number = str(unique_id_counter)
                            new_value = matrix_value
                            SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                            

                            #___existence_gap_penalty___# 15 lines down
                            the_line = grab_lines(green, file_pathway, i, 1, 15, "down")
                            first_part_removed_really_tired = delete_the_thing_in_the_string("Gap\sPenalties.\sExistence.\s", the_line)
                            existence_gap_with_newline = delete_the_thing_in_the_string(',\sExtension.\s(\d+).(\d+)', first_part_removed_really_tired)
                            existence_gap_penalty = delete_the_thing_in_the_string("(\n)", existence_gap_with_newline)
                            
                            column_name = "existence_gap_penalty"
                            id_number = str(unique_id_counter)
                            new_value = existence_gap_penalty
                            SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                            

                            #___extension_gap_penalty___# 15 lines down
                            omfg_this_is_boring = grab_lines(green, file_pathway, i, 1, 15, "down")
                            i_need_sleep = delete_the_thing_in_the_string("Gap\sPenalties.\sExistence.\s(\d+),\sExtension.\s", omfg_this_is_boring)
                            meh = delete_the_thing_in_the_string("(\n)", i_need_sleep)
                            
                            column_name = "extension_gap_penalty"
                            id_number = str(unique_id_counter)
                            new_value = meh
                            SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number)
                            
                            unique_id_counter = unique_id_counter + 1

                            
                            

    return

#   This function finds all the lines where the string_to_find variable exists
# with spaces on either side.  It returns a list with the numbers of the lines
# where string_to_find occurs.
def find_instance_line_numbers(the_file_name, file_pathway, string_to_find):
    import re
    find_this_list = [string_to_find]
    list_of_lines = []        
    for parameters in find_this_list:
        #print parameters
        patterns = [r'\b%s\b' % re.escape(parameters.strip())]
        there = re.compile('|'.join(patterns))        
        with open(file_pathway + "\\" + the_file_name + ".txt") as f:
            for i, s in enumerate(f):                
                if there.search(s):
                    #print("Line %s: %r" % (i, s))
                    list_of_lines.append(i)
    return list_of_lines
    

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
                #print "the line grabbed: ", ((the_reference_line_number + counter) - how_many_lines_from_reference)
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
#use the regular expression "(\.?\d?\d?)" to be sure to grab decimals if they are there present
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
            
    ###print put_in_table
    open_db.execute(put_in_table)
    open_db.close()
    return
    
#   Inserts one row to a table.  list_to_add and columns_to_add_to are both lists
# with the same number of items in them.  Be sure to include the id number
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
    ###print create_string

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
    open_db.close() 
    return

###This changes one value in one row in a table inside a database
##def SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number):
##    import sqlite3
##    open_db = sqlite3.connect(db_path + "\\" + db_name + ".db")
##
##    usable_string = " \'\'\'  UPDATE " + table_name + " SET " + column_name + " = \'" + new_value + '\' WHERE id = ' + str(id_number) + " \'\'\' "
##    print usable_string
##
##    open_db.execute(usable_string)
##    open_db.commit()
##    
##    open_db.close()
##    
##    return

#This changes one value in one row in a table inside a database
def SQL_UPDATE_row(db_name, db_path, table_name, column_name ,new_value, id_number):
    import sqlite3
    open_db = sqlite3.connect(db_path + "\\" + db_name + ".db")

    usable_string = "  UPDATE " + table_name + " SET " + column_name + ' = \'' + new_value + '\' WHERE id = ' +  str(id_number) + " "
    #print usable_string

    open_db.execute(usable_string)
    open_db.commit()
    
    open_db.close()
    
    return
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def main():

    the_file_name = "your_file_to_parse_name_here"
    #put the path where you put the text file below
    file_pathway = "C:\Users\Evan\Desktop\Local XML parser v2"

    local_XML_interpreter(the_file_name, file_pathway)
    
    db_name = "temp_db"
    db_path = "C:\Users\Evan\Desktop\Local XML parser v2"
    table_name = "master_table"
    SQL_SELECT_rows(db_name, db_path, table_name)

    #these open the tables inside the database                                                          
    SQL_SELECT_rows(db_name, db_path, "table_1")
    SQL_SELECT_rows(db_name, db_path, "table_2")
    SQL_SELECT_rows(db_name, db_path, "table_3")
    SQL_SELECT_rows(db_name, db_path, "table_4")
    SQL_SELECT_rows(db_name, db_path, "table_5")
    SQL_SELECT_rows(db_name, db_path, "table_6")
    SQL_SELECT_rows(db_name, db_path, "table_7")
    SQL_SELECT_rows(db_name, db_path, "table_8")
    SQL_SELECT_rows(db_name, db_path, "table_9")
    SQL_SELECT_rows(db_name, db_path, "table_10")
    SQL_SELECT_rows(db_name, db_path, "table_11")
            


main()

#------------------------------------------------------------------------------
#--------------------------------Test Case-------------------------------------
#------------------------------------------------------------------------------


#  This file is an example text file that this parser reads
# Remember that the .xml file that is output from the BLAST search
# is converted to a .txt file for this program to work.

#  This file contains one BLAST search with multiple results and several
# other BLAST searches with only one result


##
##
##BLASTN 2.2.28+
##
##
##Reference: Zheng Zhang, Scott Schwartz, Lukas Wagner, and Webb
##Miller (2000), "A greedy algorithm for aligning DNA sequences", J
##Comput Biol 2000; 7(1-2):203-14.
##
##
##
##Database: virus_file.txt
##           1,750 sequences; 60,637,755 total letters
##
##
##
##Query= 
##Length=79
##                                                                      Score     E
##Sequences producing significant alignments:                          (Bits)  Value
##
##  gi|296005648|ref|NC_014138.1| Abutilon Brazil virus DNA A, comp...   147    2e-035
##  gi|9632377|ref|NC_002048.1| Potato yellow mosaic Panama virus D...   124    9e-029
##  gi|121614279|ref|NC_008779.1| Sida yellow mosaic Yucatan virus ...   119    4e-027
##  gi|29243860|ref|NC_004638.1| Potato yellow mosaic Trinidad viru...   119    4e-027
##  gi|9629636|ref|NC_001828.1| Tomato mottle Taino virus DNA A, co...   113    2e-025
##  gi|9630683|ref|NC_001934.1| Potato yellow mosaic virus DNA A, c...   113    2e-025
##  gi|9630699|ref|NC_001938.1| Tomato mottle virus DNA A, complete...   108    9e-024
##  gi|20806520|ref|NC_003867.1| Tomato mosaic Havana virus DNA A, ...   108    9e-024
##  gi|29243836|ref|NC_004642.1| Tomato severe leaf curl virus, com...  99.0    5e-021
##  gi|39980672|ref|NC_001928.2| Abutilon mosaic virus DNA A, compl...  99.0    5e-021
##  gi|9632368|ref|NC_002046.1| Sida golden mosaic virus DNA-A, com...  97.1    2e-020
##  gi|190336474|ref|NC_010952.1| Macroptilium golden mosaic virus-...  87.9    1e-017
##  gi|21493006|ref|NC_004042.1| Bean golden mosaic virus DNA A, co...  87.9    1e-017
##  gi|20806024|ref|NC_003865.1| Melon chlorotic leaf curl virus DN...  82.4    6e-016
##
##
##> gi|296005648|ref|NC_014138.1| Abutilon Brazil virus DNA A, complete 
##genome
##Length=2653
##
## Score =  147 bits (79),  Expect = 2e-035
## Identities = 79/79 (100%), Gaps = 0/79 (0%)
## Strand=Plus/Plus
##
##Query  1     CAACGCTCAAGATTCGGATCTATTTTTATGATTCGATCACAAATTAATAAAATTTGAATT  60
##             ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
##Sbjct  939   CAACGCTCAAGATTCGGATCTATTTTTATGATTCGATCACAAATTAATAAAATTTGAATT  998
##
##Query  61    TTATTGAATGATTTTCCAG  79
##             |||||||||||||||||||
##Sbjct  999   TTATTGAATGATTTTCCAG  1017
##
##
##> gi|9632377|ref|NC_002048.1| Potato yellow mosaic Panama virus 
##DNA A, complete sequence
##Length=2584
##
## Score =  124 bits (67),  Expect = 9e-029
## Identities = 75/79 (95%), Gaps = 0/79 (0%)
## Strand=Plus/Plus
##
##Query  1    CAACGCTCAAGATTCGGATCTATTTTTATGATTCGATCACAAATTAATAAAATTTGAATT  60
##            ||||||| ||||||||||||||||||||||||||||||  ||||||||||||||| ||||
##Sbjct  876  CAACGCTTAAGATTCGGATCTATTTTTATGATTCGATCTTAAATTAATAAAATTTTAATT  935
##
##Query  61   TTATTGAATGATTTTCCAG  79
##            |||||||||||||||||||
##Sbjct  936  TTATTGAATGATTTTCCAG  954
##
##
##> gi|121614279|ref|NC_008779.1| Sida yellow mosaic Yucatan virus 
##DNA A, complete sequence
##Length=2611
##
## Score =  119 bits (64),  Expect = 4e-027
## Identities = 74/79 (94%), Gaps = 0/79 (0%)
## Strand=Plus/Plus
##
##Query  1    CAACGCTCAAGATTCGGATCTATTTTTATGATTCGATCACAAATTAATAAAATTTGAATT  60
##            ||||||| |||||||| |||||||| || ||||||||||| |||||||||||||||||||
##Sbjct  903  CAACGCTTAAGATTCGAATCTATTTCTACGATTCGATCACGAATTAATAAAATTTGAATT  962
##
##Query  61   TTATTGAATGATTTTCCAG  79
##            |||||||||||||||||||
##Sbjct  963  TTATTGAATGATTTTCCAG  981
##
##
##> gi|29243860|ref|NC_004638.1| Potato yellow mosaic Trinidad virus 
##DNA A, complete sequence
##Length=2582
##
## Score =  119 bits (64),  Expect = 4e-027
## Identities = 72/76 (95%), Gaps = 0/76 (0%)
## Strand=Plus/Plus
##
##Query  1    CAACGCTCAAGATTCGGATCTATTTTTATGATTCGATCACAAATTAATAAAATTTGAATT  60
##            ||||||| ||||||||||||||||||||||||||||||  ||||||||||||||| ||||
##Sbjct  876  CAACGCTTAAGATTCGGATCTATTTTTATGATTCGATCTTAAATTAATAAAATTTTAATT  935
##
##Query  61   TTATTGAATGATTTTC  76
##            ||||||||||||||||
##Sbjct  936  TTATTGAATGATTTTC  951
##
##
##> gi|9629636|ref|NC_001828.1| Tomato mottle Taino virus DNA A, 
##complete sequence
##Length=2597
##
## Score =  113 bits (61),  Expect = 2e-025
## Identities = 73/79 (92%), Gaps = 0/79 (0%)
## Strand=Plus/Plus
##
##Query  1    CAACGCTCAAGATTCGGATCTATTTTTATGATTCGATCACAAATTAATAAAATTTGAATT  60
##            ||||||| ||||| ||||||||||||||||||||||||   |||||||||||||||||||
##Sbjct  898  CAACGCTTAAGATCCGGATCTATTTTTATGATTCGATCTTGAATTAATAAAATTTGAATT  957
##
##Query  61   TTATTGAATGATTTTCCAG  79
##            ||||||||||||| |||||
##Sbjct  958  TTATTGAATGATTCTCCAG  976
##
##
##> gi|9630683|ref|NC_001934.1| Potato yellow mosaic virus DNA A, 
##complete sequence
##Length=2593
##
## Score =  113 bits (61),  Expect = 2e-025
## Identities = 73/79 (92%), Gaps = 0/79 (0%)
## Strand=Plus/Plus
##
##Query  1     CAACGCTCAAGATTCGGATCTATTTTTATGATTCGATCACAAATTAATAAAATTTGAATT  60
##             |||| || ||||||||||||||||||||||||||||||  |||||||||||||||  |||
##Sbjct  1030  CAACACTTAAGATTCGGATCTATTTTTATGATTCGATCTTAAATTAATAAAATTTATATT  1089
##
##Query  61    TTATTGAATGATTTTCCAG  79
##             |||||||||||||||||||
##Sbjct  1090  TTATTGAATGATTTTCCAG  1108
##
##
##> gi|9630699|ref|NC_001938.1| Tomato mottle virus DNA A, complete 
##sequence
##Length=2601
##
## Score =  108 bits (58),  Expect = 9e-024
## Identities = 64/67 (96%), Gaps = 0/67 (0%)
## Strand=Plus/Plus
##
##Query  12    ATTCGGATCTATTTTTATGATTCGATCACAAATTAATAAAATTTGAATTTTATTGAATGA  71
##             ||||| ||||||||||||||||||||||| ||||||||||||||||||||||||||||||
##Sbjct  1045  ATTCGAATCTATTTTTATGATTCGATCACGAATTAATAAAATTTGAATTTTATTGAATGA  1104
##
##Query  72    TTTTCCA  78
##             || ||||
##Sbjct  1105  TTCTCCA  1111
##
##
##> gi|20806520|ref|NC_003867.1| Tomato mosaic Havana virus DNA A, 
##complete sequence
##Length=2620
##
## Score =  108 bits (58),  Expect = 9e-024
## Identities = 68/73 (93%), Gaps = 0/73 (0%)
## Strand=Plus/Plus
##
##Query  1     CAACGCTCAAGATTCGGATCTATTTTTATGATTCGATCACAAATTAATAAAATTTGAATT  60
##             |||| || ||||| |||||||||||||||||||||||||  |||||||||||||||||||
##Sbjct  1053  CAACTCTGAAGATCCGGATCTATTTTTATGATTCGATCATGAATTAATAAAATTTGAATT  1112
##
##Query  61    TTATTGAATGATT  73
##             |||||||||||||
##Sbjct  1113  TTATTGAATGATT  1125
##
##
##> gi|29243836|ref|NC_004642.1| Tomato severe leaf curl virus, complete 
##genome
##Length=2593
##
## Score = 99.0 bits (53),  Expect = 5e-021
## Identities = 65/71 (92%), Gaps = 0/71 (0%)
## Strand=Plus/Plus
##
##Query  9    AAGATTCGGATCTATTTTTATGATTCGATCACAAATTAATAAAATTTGAATTTTATTGAA  68
##            ||||| ||||||||||||||||||||| |    |||||||||||||||||||||||||||
##Sbjct  903  AAGATCCGGATCTATTTTTATGATTCGGTATTGAATTAATAAAATTTGAATTTTATTGAA  962
##
##Query  69   TGATTTTCCAG  79
##            |||||||||||
##Sbjct  963  TGATTTTCCAG  973
##
##
##> gi|39980672|ref|NC_001928.2| Abutilon mosaic virus DNA A, complete 
##sequence
##Length=2632
##
## Score = 99.0 bits (53),  Expect = 5e-021
## Identities = 65/71 (92%), Gaps = 0/71 (0%)
## Strand=Plus/Plus
##
##Query  9     AAGATTCGGATCTATTTTTATGATTCGATCACAAATTAATAAAATTTGAATTTTATTGAA  68
##             ||||| || |||||||| ||||||||| |||  |||||||||||||||||||||||||||
##Sbjct  1075  AAGATCCGAATCTATTTCTATGATTCGCTCATGAATTAATAAAATTTGAATTTTATTGAA  1134
##
##Query  69    TGATTTTCCAG  79
##             |||||||||||
##Sbjct  1135  TGATTTTCCAG  1145
##
##
##> gi|9632368|ref|NC_002046.1| Sida golden mosaic virus DNA-A, complete 
##sequence
##Length=2642
##
## Score = 97.1 bits (52),  Expect = 2e-020
## Identities = 70/79 (89%), Gaps = 0/79 (0%)
## Strand=Plus/Plus
##
##Query  1     CAACGCTCAAGATTCGGATCTATTTTTATGATTCGATCACAAATTAATAAAATTTGAATT  60
##             |||| || ||||| || |||||||| ||||||||| | |  |||||||||||||||||||
##Sbjct  1068  CAACTCTGAAGATCCGAATCTATTTCTATGATTCGCTTATGAATTAATAAAATTTGAATT  1127
##
##Query  61    TTATTGAATGATTTTCCAG  79
##             |||||||||||||||||||
##Sbjct  1128  TTATTGAATGATTTTCCAG  1146
##
##
##> gi|190336474|ref|NC_010952.1| Macroptilium golden mosaic virus-[Jamaica:Wissadula:August 
##Town] DNA A, complete sequence
##Length=2605
##
## Score = 87.9 bits (47),  Expect = 1e-017
## Identities = 59/65 (91%), Gaps = 0/65 (0%)
## Strand=Plus/Plus
##
##Query  1    CAACGCTCAAGATTCGGATCTATTTTTATGATTCGATCACAAATTAATAAAATTTGAATT  60
##            ||||||| |||||||||||||||||||||||||||||   |||||||||||  |||||||
##Sbjct  907  CAACGCTTAAGATTCGGATCTATTTTTATGATTCGATATTAAATTAATAAAGCTTGAATT  966
##
##Query  61   TTATT  65
##            |||||
##Sbjct  967  TTATT  971
##
##
##> gi|21493006|ref|NC_004042.1| Bean golden mosaic virus DNA A, 
##complete sequence
##Length=2617
##
## Score = 87.9 bits (47),  Expect = 1e-017
## Identities = 57/62 (92%), Gaps = 0/62 (0%)
## Strand=Plus/Plus
##
##Query  12    ATTCGGATCTATTTTTATGATTCGATCACAAATTAATAAAATTTGAATTTTATTGAATGA  71
##             ||||||||||||||||||||||||||||| ||||||||||||||  ||||||||  ||||
##Sbjct  1078  ATTCGGATCTATTTTTATGATTCGATCACCAATTAATAAAATTTATATTTTATTTCATGA  1137
##
##Query  72    TT  73
##             ||
##Sbjct  1138  TT  1139
##
##
##> gi|20806024|ref|NC_003865.1| Melon chlorotic leaf curl virus 
##DNA A, complete sequence
##Length=2663
##
## Score = 82.4 bits (44),  Expect = 6e-016
## Identities = 60/68 (88%), Gaps = 0/68 (0%)
## Strand=Plus/Plus
##
##Query  9    AAGATTCGGATCTATTTTTATGATTCGATCACAAATTAATAAAATTTGAATTTTATTGAA  68
##            ||||||||||||||||||||||||||||| || ||||||||||  ||||| ||||||  |
##Sbjct  922  AAGATTCGGATCTATTTTTATGATTCGATAACCAATTAATAAATATTGAACTTTATTTTA  981
##
##Query  69   TGATTTTC  76
##            |||| |||
##Sbjct  982  TGATCTTC  989
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
##Effective search space used: 3454157535
##
##
##  Database: virus_file.txt
##    Posted date:  Jul 26, 2013  4:25 PM
##  Number of letters in database: 60,637,755
##  Number of sequences in database:  1,750
##
##
##
##Matrix: blastn matrix 1 -2
##Gap Penalties: Existence: 0, Extension: 2.5
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
##Query  1     CTCCAGCTGAATGAGACAATATATACAAGTGGGAAAAGGAGCAATACCACGGGAAAACTA  60
##             ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
##Sbjct  1261  CTCCAGCTGAATGAGACAATATATACAAGTGGGAAAAGGAGCAATACCACGGGAAAACTA  1320
##
##Query  61    ATTTGGAAGGTCAACCCCGAAATTGATACAACAATCGGGGAGTGGGCCTTCTGGGAAACT  120
##             ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
##Sbjct  1321  ATTTGGAAGGTCAACCCCGAAATTGATACAACAATCGGGGAGTGGGCCTTCTGGGAAACT  1380
##
##Query  121   aaaaaaaCCTCACTAGAAAA  140
##             ||||||||||||||||||||
##Sbjct  1381  AAAAAAACCTCACTAGAAAA  1400
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
