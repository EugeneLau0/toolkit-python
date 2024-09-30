CREATE TABLE IF NOT EXISTS test_table (
    id BIGSERIAL PRIMARY KEY,
    materialid BIGINT DEFAULT 0,
    stockid BIGINT DEFAULT 0,
    spaceid BIGINT DEFAULT 0,
    auxpropid BIGINT DEFAULT 0,
    batchno VARCHAR DEFAULT '',
    kfdata VARCHAR DEFAULT '',
    validate VARCHAR DEFAULT '',
    qty NUMERIC DEFAULT 0,
    validqty NUMERIC DEFAULT 0,
    CONSTRAINT unique_material_stock_space_auxprop_batch_kfdata_validate UNIQUE (materialid, stockid, spaceid, auxpropid, batchno, kfdata, validate)
);
