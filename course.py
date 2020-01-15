class Course:
    
  def __init__(self,code,is_recent=True,is_co=False,req_ss=None,min_UOC=0):
    self.code = code
    self.is_co = is_co
    self.req_ss = req_ss
    self.min_UOC = 0
    self.is_recent = True

  
    
