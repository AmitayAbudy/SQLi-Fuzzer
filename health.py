from sql_creator import strings, stage_one_chars

def check_stage(string_id):
    """
    This function gets a string and returns its current stage and grades
    """
    strings[string_id] = 

def calculate(string_id):
  """
  This function gets a string and returns it's health value
  """
  chars = list(s)
  health_grade = 0
  stage = check_stage(s)


  for char in chars:
      if char in stage_one_chars:
          health_grade += 1
  return health_grade




print(calculate("1234567890"))
