"""
Blockchain simulation for Medical Report Management System.
Implements a simple blockchain using SHA-256 hashing stored in SQLite.
"""
import hashlib
import json
from datetime import datetime


class Block:
    """Represents a single block in the blockchain."""

    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.data_hash = self._hash_data(data)
        self.previous_hash = previous_hash
        self.block_hash = self.calculate_hash()

    def _hash_data(self, data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def calculate_hash(self):
        content = f"{self.index}{self.timestamp}{self.data_hash}{self.previous_hash}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()


class Blockchain:
    """Manages the blockchain stored in SQLite."""

    def __init__(self, db):
        self.db = db
        count = db.execute('SELECT COUNT(*) FROM blockchain').fetchone()[0]
        if count == 0:
            self._create_genesis_block()

    def _create_genesis_block(self):
        genesis_data = json.dumps({
            'action': 'GENESIS',
            'details': 'Medical Blockchain Initialized'
        })
        block = Block(0, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                      genesis_data, '0' * 64)
        self._save_block(block)

    def _save_block(self, block):
        self.db.execute('''INSERT INTO blockchain
            (block_index, timestamp, data, data_hash, previous_hash, block_hash)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (block.index, block.timestamp, block.data,
             block.data_hash, block.previous_hash, block.block_hash))
        self.db.commit()

    def add_block(self, action_type, details):
        last = self.db.execute(
            'SELECT block_index, block_hash FROM blockchain ORDER BY id DESC LIMIT 1'
        ).fetchone()
        new_index = last['block_index'] + 1
        previous_hash = last['block_hash']

        data = json.dumps({
            'action': action_type,
            'details': details,
        })
        block = Block(new_index,
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                      data, previous_hash)
        self._save_block(block)
        return block

    def get_chain(self):
        rows = self.db.execute(
            'SELECT * FROM blockchain ORDER BY block_index ASC'
        ).fetchall()
        return rows

    def get_latest_block(self):
        return self.db.execute(
            'SELECT * FROM blockchain ORDER BY id DESC LIMIT 1'
        ).fetchone()

    def verify_chain(self):
        """Verify the integrity of the entire blockchain."""
        rows = self.db.execute(
            'SELECT * FROM blockchain ORDER BY block_index ASC'
        ).fetchall()
        errors = []
        for i, row in enumerate(rows):
            # Verify block hash
            content = f"{row['block_index']}{row['timestamp']}{row['data_hash']}{row['previous_hash']}"
            expected_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
            if row['block_hash'] != expected_hash:
                errors.append(f"Block {row['block_index']}: hash mismatch")

            # Verify data hash
            expected_data_hash = hashlib.sha256(
                row['data'].encode('utf-8')).hexdigest()
            if row['data_hash'] != expected_data_hash:
                errors.append(f"Block {row['block_index']}: data hash mismatch")

            # Verify chain link (skip genesis)
            if i > 0:
                if row['previous_hash'] != rows[i - 1]['block_hash']:
                    errors.append(
                        f"Block {row['block_index']}: broken chain link")

        is_valid = len(errors) == 0
        return is_valid, errors, len(rows)


def hash_file(file_path):
    """Compute SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()
