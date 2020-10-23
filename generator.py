class OwnRange:
    def __init__(self,start,end=None):
        if end is None:
            self.end=start
            self.start=0
            
        else:
            self.start=start
            self.end=end
        self.current=self.start    
    def __str__(self):
        return "this is our own range from {} to {}".format(self.start,self.end) 
    
    
    def __next__(self):
        if self.current==self.end:
            raise StopIteration
        v=self.current
        self.current+=1
        return v
    def __iter__(self):
        return self
    
def generator(start,end):
    current=start
    while current<end:
        yield current
        current+=1
            


    
if __name__=="__main__":
    x=OwnRange(20)
    for i in x:
        print(i)
  
    g=generator(1,20)
    print(next(g))
    print(next(g))
    print(next(g))
    print(next(g))
    for i in generator(3,10):
       print(i)

            