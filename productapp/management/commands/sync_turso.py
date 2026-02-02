from django.core.management.base import BaseCommand
import subprocess
import json
import sqlite3
from django.conf import settings
import os


class Command(BaseCommand):
    help = "Sync local SQLite database with Turso cloud database using Node.js"

    def handle(self, *args, **options):
        self.stdout.write("Starting Turso database sync via Node.js...")

        # Node.js script to sync data
        node_script = f"""
const {{ createClient }} = require('@libsql/client');

async function syncData() {{
  try {{
    const client = createClient({{
      url: '{settings.TURSO_URL}',
      authToken: '{settings.TURSO_AUTH_TOKEN}'
    }});
    
    const tables = [
      'productapp_product', 
      'auth_user', 
      'productapp_cart', 
      'productapp_ordercart', 
      'productapp_selection', 
      'custom_design', 
      'productapp_shop', 
      'productapp_magazine'
    ];
    
    const allData = {{}};
    
    for (const table of tables) {{
      try {{
        const result = await client.execute(`SELECT * FROM ${{table}}`);
        allData[table] = {{
          columns: result.columns,
          rows: result.rows
        }};
        console.log(`Synced ${{table}}: ${{result.rows.length}} records`);
      }} catch (e) {{
        console.log(`Could not sync ${{table}}: ${{e.message}}`);
        allData[table] = {{ columns: [], rows: [] }};
      }}
    }}
    
    await client.close();
    console.log('DATA_START:' + JSON.stringify(allData));
  }} catch (error) {{
    console.error('Sync error:', error.message);
    process.exit(1);
  }}
}}

syncData();
"""

        try:
            # Run Node.js script
            result = subprocess.run(
                ["node", "-e", node_script],
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
            )

            if result.returncode != 0:
                self.stdout.write(self.style.ERROR(f"Node.js error: {result.stderr}"))
                return

            # Parse the data from Node.js output
            output_lines = result.stdout.strip().split("\n")
            data_line = None

            for line in output_lines:
                if line.startswith("DATA_START:"):
                    data_line = line[11:]  # Remove 'DATA_START:' prefix
                    break

            if not data_line:
                self.stdout.write(self.style.ERROR("No data received from Node.js"))
                return

            all_data = json.loads(data_line)

            # Connect to local SQLite
            local_db_path = settings.DATABASES["default"]["NAME"]
            local_conn = sqlite3.connect(local_db_path)

            try:
                for table_name, table_data in all_data.items():
                    if table_data["rows"]:
                        # Clear local table
                        local_conn.execute(f"DELETE FROM {table_name}")

                        # Prepare insert statement
                        columns = table_data["columns"]
                        if columns:
                            placeholders = ", ".join(["?" for _ in columns])
                            insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

                            # Insert data
                            for row in table_data["rows"]:
                                row_data = tuple(row[col] for col in columns)
                                local_conn.execute(insert_sql, row_data)

                    self.stdout.write(
                        f"Imported {table_name}: {len(table_data['rows'])} records"
                    )

                # Commit changes
                local_conn.commit()
                self.stdout.write(
                    self.style.SUCCESS("Turso sync completed successfully!")
                )

            finally:
                local_conn.close()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Sync failed: {str(e)}"))
