from flask import Flask, request, jsonify
import Util.bd as bd

app = Flask(__name__)

@app.route('/territories', methods=['POST'])
def create_territory():
    data = request.get_json()
    conn = bd.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO territories (territory_id, territory_description, region_id)
            VALUES (%s, %s, %s, %s)
            """,
            (data['territory_id'], data['territory_description'], data.get('region_id'))
        )
        conn.commit()
        return jsonify({"message": "territory created successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/territories/<int:territory_id>', methods=['GET'])
def read_territory(territory_id):
    conn = bd.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM territories WHERE territory_id = %s", (territory_id,))
        territory = cursor.fetchone()
        if territory is None:
            return jsonify({"error": "territory not found"}), 404
        return jsonify({
            "territory_id": territory[0],
            "territory_description": territory[1],
            "region_id": territory[2],
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/territories/<int:territory_id>', methods=['PUT'])
def update_territory(territory_id):
    data = request.get_json()
    conn = bd.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE territories
            SET territory_description = %s, region_id = %s
            WHERE territory_id = %s
            """,
            (data['territory_description'], data.get('region_id'), territory_id)
        )
        conn.commit()
        return jsonify({"message": "territory updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/territories/<int:territory_id>', methods=['DELETE'])
def delete_territory(territory_id):
    conn = bd.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM territories WHERE territory_id = %s", (territory_id,))
        conn.commit()
        return jsonify({"message": "territory deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)