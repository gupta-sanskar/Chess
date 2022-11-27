from django.db import models

# Create your models here.
class GameMoves(models.Model):
  piecemoves = models.TextField(blank=True)

  def set_list(self, move):
    self.piecemoves += "," + move if self.piecemoves else move

  def get_list(self):
    return self.piecemoves.split(",") if self.piecemoves else None
