import h5py
import xapi.lo
from utils.group import LeanDataset, LeanGroup

class InteractionCreator():
    def __init__(self, bundle, statement):
        self.statement = statement
        self.bundle = bundle
        self.id = None
        self.extract_id()

    @property
    def path(self):
        return '/interaction/{}/{}'.format(self.id[0], self.id[1])

    def extract_id(self):
        if self.verb.id.startswith('http://adlnet.gov/expapi/verbs'):
            auth = "adl"
            id = verb.id[31:]
        else:
            auth = verb.id[7:]
            auth = auth[:auth.find('/')]
            id = verb.id[verb.id.rfind('/'):]
        self.id = (auth, id)

    def create(self):
        path = self.path
        if path in self.bundle:
            grp = self.bundle[path]
            self.check_definition(grp)
        else:
            grp = self.bundle.create_group(path)
            self.write_definition(grp)
        return grp

    def write_definiton(self):
        pass

    def check_definition(self, group):
        pass



def create(fibers, bundle, statement):
    #create an interaction if not present, link to it
    (auth, id) = _extract_id(statement.verb)
    #print("Interaction is {}/{}".format(auth,id))
    #TODO: Add display/description to interaction
    interaction = InteractionCreator(bundle, statement).create()
    #TODO: Check if we want to automatically trace uses!?
    #create data for fiber
    data = [interaction.ref]
    #create a learning object based on the object (if it does not refer to a user or another statement)
    object = statement.object
    #print("Type: {}".format(object.objectType.lower()))
    if object.objectType.lower() == 'activity':
        #object references an lo
        #create it
        learning_object = lo.create(bundle, statement)
        data.append(learning_object.ref)
        #print("Created activity entry")
    else:
        raise NotImplementedError(object.objectType, "not implemented yet")
    #store refs in fiber
    dset = fibers.create_dataset('interaction', (len(data),), dtype=REF_DT)
    dset[...] = data
