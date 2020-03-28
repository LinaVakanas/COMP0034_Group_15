### Things to do ###
* What goes in 
    - medication form
    - personal issues => kinda did
    - hobbies
* Pair mentee, mentor randomly => doing
* Put character limits in
* instead of flashing to home page for mentor out of London, redirect to another page, and then have button for home?
* Refactor => make code more concise. 
    - A lot of the stuff are repeated b/c of mentor/mentee, w/ only difference being 
whether it says mentor or mentee, and the if statement ==> define separate functions?
* Improve quality code
    - Make code less vulnerable to errors
    - Sometimes variables called with possibility of them not being defined (bc created in if loops)
    - When to pass mentee/mentor and user? 
* Should we have the personal form after the general signup? (name, last name, email)
it could make testing more specific, and the form.validate_on_submit

To ask Miss:
* Updating user id --> models
* Passing in applicant type (for real would be in url)
* None or ''
* Using an externally downloaded file --> how to reference (directory)
* Form not being validated in tests? (2 empty parts not used, but not DataRequired())
* 'Dummy' data made in unittest SetUp not being saved?
* Half foreign half primary key? (meeting table) 

------------------------------------------------------------
To Do Before Move On:
* Validators for forms in util>validators.py
* Filter by paired status
* Signup linked to school database - if school_id isn't saved in database --> validators.py

    

