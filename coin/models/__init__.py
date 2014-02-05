from coin import db
class BaseModel(db.Model):

  def get_public_data(self):
    data = self._data

    return data
