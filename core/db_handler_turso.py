#!/usr/bin/env python3
"""
Database handler for Prakrit verb and noun forms - Turso/libSQL version.
Optimized for Vercel deployment with Turso edge database.
"""

import os
import random
from typing import List, Dict, Optional

try:
    from libsql_client import create_client
    HAS_LIBSQL = True
except ImportError:
    HAS_LIBSQL = False
    print("⚠️ libsql-client not installed. Install with: pip install libsql-client")

from core.script_converter import ScriptConverter


class PrakritDatabaseTurso:
    """Handles database operations using Turso (libSQL) for edge deployment."""

    def __init__(self, turso_url=None, turso_token=None):
        """
        Initialize Turso database connection.

        Args:
            turso_url: Turso database URL (e.g., libsql://your-db.turso.io)
            turso_token: Turso authentication token
        """
        self.converter = ScriptConverter()
        self.connected = False

        # Get credentials from args or environment
        self.turso_url = turso_url or os.getenv('TURSO_DATABASE_URL')
        self.turso_token = turso_token or os.getenv('TURSO_AUTH_TOKEN')

        if not HAS_LIBSQL:
            raise ImportError("libsql-client is required. Install with: pip install libsql-client")

        if not self.turso_url or not self.turso_token:
            raise ValueError("Turso URL and token are required. Set TURSO_DATABASE_URL and TURSO_AUTH_TOKEN")

        try:
            # Create Turso client
            self.client = create_client(
                url=self.turso_url,
                auth_token=self.turso_token
            )
            self.connected = True
            print("✓ Connected to Turso database")
        except Exception as e:
            print(f"✗ Turso connection failed: {e}")
            raise

    def _execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute a query and return results as list of dicts."""
        try:
            if params:
                result = self.client.execute(query, params)
            else:
                result = self.client.execute(query)

            # Convert result to list of dicts
            if hasattr(result, 'rows') and result.rows:
                columns = result.columns if hasattr(result, 'columns') else []
                return [dict(zip(columns, row)) for row in result.rows]
            return []
        except Exception as e:
            print(f"Query error: {e}")
            return []

    def _execute_single(self, query: str, params: tuple = None) -> Optional[Dict]:
        """Execute query and return single result."""
        results = self._execute_query(query, params)
        return results[0] if results else None

    # ===== VERB METHODS =====

    def get_verb_form(self, root: str, tense: str, person: str, number: str,
                      script: str = 'devanagari') -> Optional[str]:
        """Get a specific verb form."""
        query = '''
            SELECT vf.form
            FROM verbs v
            JOIN verb_forms vf ON v.id = vf.verb_id
            WHERE v.root = ? AND vf.tense = ? AND vf.person = ? AND vf.number = ?
        '''
        result = self._execute_single(query, (root, tense, person, number))

        if result:
            form_hk = result['form']
            return self.converter.convert(form_hk, 'hk', script)
        return None

    def get_random_verb_form(self, difficulty: str = None, script: str = 'devanagari') -> Optional[Dict]:
        """Get a random verb form with full context."""
        # Get random verb
        if difficulty:
            verb_query = "SELECT * FROM verbs WHERE difficulty = ? ORDER BY RANDOM() LIMIT 1"
            params = (difficulty,)
        else:
            verb_query = "SELECT * FROM verbs ORDER BY RANDOM() LIMIT 1"
            params = None

        verb = self._execute_single(verb_query, params)
        if not verb:
            return None

        # Get random form of this verb
        form_query = "SELECT * FROM verb_forms WHERE verb_id = ? ORDER BY RANDOM() LIMIT 1"
        form_data = self._execute_single(form_query, (verb['id'],))

        if not form_data:
            return None

        return {
            'form': self.converter.convert(form_data['form'], 'hk', script),
            'form_hk': form_data['form'],
            'root': self.converter.convert(verb['root'], 'hk', script),
            'root_hk': verb['root'],
            'meaning': verb['meaning'],
            'tense': form_data['tense'],
            'person': form_data['person'],
            'number': form_data['number'],
            'transitivity': verb['transitivity'],
            'difficulty': verb['difficulty']
        }

    def get_all_verbs(self, script: str = 'devanagari') -> List[Dict]:
        """Get list of all verbs."""
        query = "SELECT id, root, meaning, transitivity, difficulty FROM verbs"
        verbs = self._execute_query(query)

        return [{
            'id': v['id'],
            'root': self.converter.convert(v['root'], 'hk', script),
            'root_hk': v['root'],
            'meaning': v['meaning'],
            'transitivity': v['transitivity'],
            'difficulty': v['difficulty']
        } for v in verbs]

    # ===== NOUN METHODS =====

    def get_noun_form(self, root: str, case_name: str, number: str,
                      script: str = 'devanagari') -> Optional[str]:
        """Get a specific noun form."""
        query = '''
            SELECT nf.form
            FROM nouns n
            JOIN noun_forms nf ON n.id = nf.noun_id
            WHERE n.root = ? AND nf.case_name = ? AND nf.number = ?
        '''
        result = self._execute_single(query, (root, case_name, number))

        if result:
            form_hk = result['form']
            return self.converter.convert(form_hk, 'hk', script)
        return None

    def get_random_noun_form(self, difficulty: str = None, script: str = 'devanagari') -> Optional[Dict]:
        """Get a random noun form with full context."""
        # Get random noun
        if difficulty:
            noun_query = "SELECT * FROM nouns WHERE difficulty = ? ORDER BY RANDOM() LIMIT 1"
            params = (difficulty,)
        else:
            noun_query = "SELECT * FROM nouns ORDER BY RANDOM() LIMIT 1"
            params = None

        noun = self._execute_single(noun_query, params)
        if not noun:
            return None

        # Get random form
        form_query = "SELECT * FROM noun_forms WHERE noun_id = ? ORDER BY RANDOM() LIMIT 1"
        form_data = self._execute_single(form_query, (noun['id'],))

        if not form_data:
            return None

        return {
            'form': self.converter.convert(form_data['form'], 'hk', script),
            'form_hk': form_data['form'],
            'root': self.converter.convert(noun['root'], 'hk', script),
            'root_hk': noun['root'],
            'meaning': noun['meaning'],
            'case': form_data['case_name'],
            'number': form_data['number'],
            'gender': noun['gender'],
            'difficulty': noun['difficulty']
        }

    def get_all_nouns(self, script: str = 'devanagari') -> List[Dict]:
        """Get list of all nouns."""
        query = "SELECT id, root, meaning, gender, difficulty FROM nouns"
        nouns = self._execute_query(query)

        return [{
            'id': n['id'],
            'root': self.converter.convert(n['root'], 'hk', script),
            'root_hk': n['root'],
            'meaning': n['meaning'],
            'gender': n['gender'],
            'difficulty': n['difficulty']
        } for n in nouns]

    def get_noun_paradigm(self, root: str, script: str = 'devanagari') -> Dict:
        """Get all forms of a noun (full declension table)."""
        query = '''
            SELECT nf.case_name, nf.number, nf.form
            FROM nouns n
            JOIN noun_forms nf ON n.id = nf.noun_id
            WHERE n.root = ?
        '''
        results = self._execute_query(query, (root,))

        paradigm = {}
        for row in results:
            case_name = row['case_name']
            number = row['number']
            form = self.converter.convert(row['form'], 'hk', script)

            if case_name not in paradigm:
                paradigm[case_name] = {}
            paradigm[case_name][number] = form

        return paradigm

    def get_random_noun(self, difficulty: str = None, script: str = 'devanagari') -> Optional[Dict]:
        """Get a random noun with its metadata."""
        if difficulty:
            query = "SELECT * FROM nouns WHERE difficulty = ? ORDER BY RANDOM() LIMIT 1"
            params = (difficulty,)
        else:
            query = "SELECT * FROM nouns ORDER BY RANDOM() LIMIT 1"
            params = None

        noun = self._execute_single(query, params)
        if not noun:
            return None

        return {
            'id': noun['id'],
            'root': self.converter.convert(noun['root'], 'hk', script),
            'root_hk': noun['root'],
            'meaning': noun['meaning'],
            'gender': noun['gender'],
            'difficulty': noun['difficulty']
        }

    def close(self):
        """Close database connection."""
        if hasattr(self, 'client') and self.client:
            try:
                self.client.close()
            except:
                pass


# Test if run directly
if __name__ == '__main__':
    print("Testing Turso Database Handler:")
    print("="*60)

    turso_url = os.getenv('TURSO_DATABASE_URL')
    turso_token = os.getenv('TURSO_AUTH_TOKEN')

    if not turso_url or not turso_token:
        print("❌ Set TURSO_DATABASE_URL and TURSO_AUTH_TOKEN environment variables")
        exit(1)

    try:
        db = PrakritDatabaseTurso(turso_url, turso_token)

        # Test verb retrieval
        print("\n1. Testing verb form retrieval:")
        form = db.get_verb_form('pac', 'present', 'first', 'singular', script='devanagari')
        print(f"  pac (present, 1st, singular) in Devanagari: {form}")

        # Test random verb form
        print("\n2. Testing random verb form:")
        random_verb = db.get_random_verb_form(script='devanagari')
        if random_verb:
            print(f"  Root: {random_verb['root']} ({random_verb['meaning']})")
            print(f"  Form: {random_verb['form']}")
            print(f"  Grammar: {random_verb['tense']}, {random_verb['person']}, {random_verb['number']}")

        # Test noun retrieval
        print("\n3. Testing noun form retrieval:")
        noun_form = db.get_noun_form('dhamma', 'nominative', 'singular', script='devanagari')
        print(f"  dhamma (nominative, singular) in Devanagari: {noun_form}")

        # Test random noun form
        print("\n4. Testing random noun form:")
        random_noun = db.get_random_noun_form(script='devanagari')
        if random_noun:
            print(f"  Root: {random_noun['root']} ({random_noun['meaning']})")
            print(f"  Form: {random_noun['form']}")
            print(f"  Grammar: {random_noun['case']}, {random_noun['number']}, {random_noun['gender']}")

        print("\n" + "="*60)
        print("✓ Turso database tests completed successfully!")

        db.close()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
