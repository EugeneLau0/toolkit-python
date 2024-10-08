import time

import db_util as db

class InventoryItem:
    def __init__(self, id: int, materialid: int = 0, stockid: int = 0, 
                 spaceid: int = 0, auxpropid: int = 0, batchno: str = '', 
                 kfdata: str = '', validate: str = '', qty: float = 0, 
                 validqty: float = 0):
        self.id = id
        self.materialid = materialid
        self.stockid = stockid
        self.spaceid = spaceid
        self.auxpropid = auxpropid
        self.batchno = batchno
        self.kfdata = kfdata
        self.validate = validate
        self.qty = qty
        self.validqty = validqty

def create_inventory_item(unique_id: int) -> InventoryItem:
    return InventoryItem(
        id=unique_id,
        materialid=unique_id,
        stockid=unique_id,
        spaceid=unique_id,
        auxpropid=unique_id,
        batchno='',
        kfdata='',
        validate='',
        qty=1,
        validqty=1
    )

def upsert_inventory_item(config, items: list):
    sql = f"""
    INSERT INTO test_table (materialid, stockid, spaceid, auxpropid, batchno, kfdata, validate, qty, validqty)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (materialid, stockid, spaceid, auxpropid, batchno, kfdata, validate) 
    DO UPDATE SET
        qty = test_table.qty + EXCLUDED.qty,
        validqty = test_table.validqty + EXCLUDED.validqty;
    """
    # 记录执行耗时
    start_time = time.time()
    db.execute_sql_with_params(config=config, sql=sql, inventory_items=items)
    end_time = time.time()
    return round(end_time - start_time, 2)

def insert_inventory_item(config, items: list):
    insert_sql = f"""
    INSERT INTO test_table (materialid, stockid, spaceid, auxpropid, batchno, kfdata, validate, qty, validqty)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (materialid, stockid, spaceid, auxpropid, batchno, kfdata, validate) 
    DO NOTHING
    """

    values_list = []
    for item in items:
        values_list.append(f"({item.materialid}, {item.stockid}, {item.spaceid}, {item.auxpropid}, "
                           f"'{item.batchno}', '{item.kfdata}', '{item.validate}', "
                           f"{item.qty}, {item.validqty})")
    
    values_str = ", ".join(values_list)

    update_sql = f"""
    UPDATE test_table
    SET 
        qty = test_table.qty + updates.new_qty,
        validqty = test_table.validqty + updates.new_validqty
    FROM (
        VALUES {values_str}
    ) AS updates(materialid, stockid, spaceid, auxpropid, batchno, kfdata, validate, new_qty, new_validqty)
    WHERE test_table.materialid = updates.materialid
      AND test_table.stockid = updates.stockid
      AND test_table.spaceid = updates.spaceid
      AND test_table.auxpropid = updates.auxpropid
      AND test_table.batchno = updates.batchno
      AND test_table.kfdata = updates.kfdata
      AND test_table.validate = updates.validate;
    """

    # 记录执行耗时  
    start_time = time.time()
    # 先insert
    db.execute_sql_with_params(config=config, sql=insert_sql, inventory_items=items)
    # 再update
    db.execute_sql(config=config, sql=update_sql)
    end_time = time.time()
    return round(end_time - start_time, 2)

