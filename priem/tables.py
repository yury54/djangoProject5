from priem.models import Register
from table import Table
from table.columns import Column
from table.columns import LinkColumn, Link
from table.utils import A

class PersonTable(Table):
    r_date = Column(field='r_date', header='Дата',header_attrs={'width': '10%'})
    stol = Column(field='stol', header='Стол №', header_attrs={'width': '10%'})
    time = Column(field='time', header='Время', header_attrs={'width': '10%'})
    fio = Column(field='fio', header='ФИО', header_attrs={'width': '30%'})
    subject = Column(field='subject', header='Причина обращения')
    action = LinkColumn(header='Удалить', links=[Link(text='Удалить', viewname='edit', args=(A('id'),)),])
    class Meta:
        model = Register
        sort = [(0, 'asc'), (1, 'asc'),(2, 'asc')]

