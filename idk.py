
Is in cache?

    Yes: Return cache data.

    No:
        Aqcuire lock in CityLock to add to dict
            
            if not present as key
                
                add to dict with lock instance,return dict value
        
        Release lock in CityLock
        
        Aqcuire Shared Lock
            
            if lock returned from CityLock
                
                aqcuire lock returned from CityLock
            
            Is in cache check again?

                Yes: Release shared lock, return data.

                No:

                    Fetch Weather API Data

                    Add to Cache Dictionary
                    
                    Release Lock from CityLock

                    Return Data
