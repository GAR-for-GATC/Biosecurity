#BLASTn with XML parser v2.1
#8/11/2013
# By: Evan Weaver

#    This program will take a sequence imputed from the user and runs a BLAST
# serach against a local database and return the resuts as an XML file.
# Then the .xml file is changed to a .txt file and the results are parsed
# into a SQLite3 database.  The results from the SQL database are then printed
# onto the screen.
#Note: This program only does BLASTn searches against a nucleotide database

##How to use##
#1) Install python
#2) Install the matching version of Biopython
#3) Create a BLAST database using the makeblastdb application
#   or use the "BLAST fasta compiler.py" program to compile
#   a large notepad file to feed into the makeblastdb program
#   to create a larger BLAST database to search from.
#4) Make sure that the database you created has no spaces.
#5) Stick the three database files into a folder.
#6) Run the program and follow the directions.
#7) The program will create 2 text files and one database file.
#   it does not delete them automatically so you can check the
#   .xml parser for errors.
#8) The results printed are the values stored in the SQLdatabase
#   the tables in which the values are stored are printed as well.
#   Note: The master_table, printed as a result, shows what other
#   tables are in the database.
#9) Since individual values are not labeled in the results printed,
#   you will need to use the SELECT sql command to select values from
#   inside the database.  Future versions may use a GUI to simplify
#   accessing of the database, but you will have to do this manually.
#   Here is a good video explanation: http://www.youtube.com/watch?v=Ll_ufNL5rDA
#   If the link is broken, the video is called: Python 2.7 Tutorial Pt 12 SQLite
#   The tutorial for sqlite was done by: Derek Banas
#10) In order to run the program multiple times, you will need to move or
#   delete the text files and database file created by the previous run.



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~Functions which obtain user input~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def Gets_User_Query():   
    My_Query = raw_input("Enter your DNA query: ")
    
    return My_Query

def Get_BLAST_stuff():
    print "Enter the BLAST database folder path (ex: C:/Users/Evan/Desktop)"
    print "Do not add a backslash on the end of the path."
    print "  Be sure to elimate spaces in the path. Biopython's BLAST wrapper"
    print "does not like spaces."
    print "(ex: C:/User/Purple_dragon is ok, but C:/User/Purple dragon  is not ok)"
    print "  Also, be sure to insert the database, which is made up of three"
    print "files, into it's own folder. You need to enter the pathway to the folder, "
    print "NOT the database files."
    print "(ex: C:/User/Purple_dragon contains the folder my_database which"
    print "contains the three BLAST database files.)"
    print "If you copy/paste parameters, paste as plain text to remove newlines"
    BLAST_db_path = raw_input(": ")
    print " "
    print "Enter the folder name in which the BLAST database files reside."
    print "Resist the urge to add slashes anywhere in the folder name."
    print "Your database folder name needs have no spaces in it."
    BLAST_db_folder_name = raw_input(": ")
    print " "
    print "Enter your database name."
    print "  Do not add any extensions to the end of the database name."
    print "(ex .db . nin .txt etc.)"
    print "  To get this, use the name of the .nin, .nhr or .nsq files if"
    print "you're working with a nucleotide database"
    print "Your database name also needs to have no spaces in it."
    BLAST_db_name = raw_input(": ")
    
    return BLAST_db_path, BLAST_db_name, BLAST_db_folder_name
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~Functions used by BLAST searches~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def Puts_the_query_in_a_text_doc_so_BLAST_can_use_it(My_Query, db_path):  

    my_stuff = open(db_path + "\\" + "temporary_file.txt", "w")
    my_stuff.write(My_Query)
    my_stuff.close
    return "temporary_file.txt"

def Deletes_the_temporary_file(db_path): #This deletes the temporary_file.txt file
    import os
    os.remove(db_path + "\\"+ "temporary_file.txt")
    return
def Changes_backslashes_to_forward_slashes(my_string):
    import re
    #   Sticking an "r" in front of the string creates a raw string
    # Raw strings use different rules to interpret backslashes.
    # Putting a "u" in front of the string will create a unicode string
    # In python 3, putting a "b" in front of a string will create a byte literal
    what_to_find = re.compile(r"\\")
    find_backslashes = re.findall(what_to_find, my_string)
    split_string = what_to_find.split(my_string)
    my_sub = what_to_find.sub("/", my_string)
    
    return my_sub

    
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~BLAST searches~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def Runs_local_BLASTn_search(My_Query, BLAST_db_path, BLAST_db_folder_name, BLAST_db_name):
    Puts_the_query_in_a_text_doc_so_BLAST_can_use_it(My_Query, BLAST_db_path)

    
    # Changes_backslashes_to_forward_slashes function creates
    # strings to input into the Ncbiblast Commandline biopython module.
    BLAST_db_path_no_backslash = Changes_backslashes_to_forward_slashes(BLAST_db_path)
    BLAST_db_name_no_backslash = Changes_backslashes_to_forward_slashes(BLAST_db_name)
    
    blastncline = NcbiblastnCommandline(query= (BLAST_db_path_no_backslash + "/" + "temporary_file.txt"), db = (BLAST_db_path_no_backslash + "/" + BLAST_db_folder_name + "/" + BLAST_db_name_no_backslash), out = (BLAST_db_path_no_backslash + "/my_xml.xml"))
    #NcbiblastnCommandline doesn't like python variables, only strings.  The only input is temporary_file.txt anyway
    #NcbiblastnCommandline also doesn't like spaces inside the file pathways
    #  NcbiblastnCommandline doesn't like backslashes in the file pathways (\).
    # Be sure to change all basckslashes to forwardslashes prior to using NcbiblastnCommandline.
    blastncline()
    
    Deletes_the_temporary_file(BLAST_db_path) #Deletes the temporary text file
    
    return
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~Local XML Parser v2~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
                            print "_______________________________________________________________________"
                            print '_______________________________________________________________________'
                            print "No hits found in one BLAST search."
                            print "   The BLAST search with no hits will not have the "
                            print "following values in it's SQL table."
                            print " "
                            print "sequence_length, sequence_fasta_name, score_value, expect_value, "
                            print "identities_value, gaps_value, strand_value, subject_and_query_lines."
                            print "_______________________________________________________________________"
                            print "_______________________________________________________________________"
                        
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

def SQLite_table_names_in_a_db(db_name, db_path):
    import sqlite3
    import re

    con = sqlite3.connect(db_path + "\\" + db_name + ".db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
    #print(cursor.fetchall())
    put_stuff_here = []
    for i in cursor.fetchall():
        #print i
        put_stuff_here.append(str(i))
    #print put_stuff_here
    list_of_tables = []
    for purple in put_stuff_here:
        find_the_table = re.findall("CREATE TABLE\s(.+)\s.id", purple)
        for q in find_the_table:
            #print "meh ", q
            list_of_tables.append(q)
    
    return list_of_tables
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



def Change_filetype_to_txt(my_filename, my_filepath):
    import os
    file_and_path = my_filepath + "\\" + my_filename + ".xml"
    
    base = os.path.splitext(file_and_path)[0]
    os.rename(file_and_path, base + ".txt")
    return


def Open_the_XML_file():  #works
    import os
    os.startfile("C:/Users/Evan/Desktop/local_BLASTn_with_XML__parser_v2/my_xml.xml")
    return


def main():
    from Bio.Blast.Applications import NcbiblastnCommandline
    the_query = Gets_User_Query()
    BLAST_db_path, BLAST_db_name, BLAST_db_folder_name = Get_BLAST_stuff()
    
    Runs_local_BLASTn_search(the_query, BLAST_db_path, BLAST_db_name, BLAST_db_folder_name)
    #Open_the_XML_file()
    
    the_file_name = "my_xml"
    #file_pathway = "C:/Users/Evan/Desktop/local_BLASTn_with_XML__parser_v2"
    Change_filetype_to_txt(the_file_name, BLAST_db_path)
    
    local_XML_interpreter(the_file_name, BLAST_db_path)
    
    db_name = "temp_db"
    db_path = BLAST_db_path
    my_tables = SQLite_table_names_in_a_db(db_name, db_path)
    for i in my_tables:
        print "Table in database: ", i
        SQL_SELECT_rows(db_name, db_path, i)


    
main()
