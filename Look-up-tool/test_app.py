from database import connect
import unittest
import json
import app
from utility import if_id_exist


class TestApp(unittest.TestCase):
    ##test if correctly get info online
    def test_if_id_legit(self):
        client = connect()
        id = 154432
        result = if_id_exist(client, id, True)
        json_data = json.loads(result)
        self.assertEqual("Rebecca Ore", json_data[0]["author name"])
    def test_correct_get(self):
        with app.app.test_client() as client:
            json_test = client.get('/book?id=51285942').get_json(force=True) ##this is the example of bloddy sunset
        temp = json.loads(json_test)
        bool = "Bloody Sunset" in temp[0]['title']
        self.assertTrue(bool)

    #i was intended to write a test case for delete, but turns out that it is impossible to test!
    '''
    def test_correct_delete(self):
        with app.app.test_client() as client:
            json_test = client.delete('/book?id=51285942').get_json(force=True) ##this is the example of bloddy sunset
    '''
    
        

        
        
if __name__ == '__main__':
    unittest.main()
    