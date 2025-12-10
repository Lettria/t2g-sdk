import os
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=os.getenv("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


class Neo4jService:
    @staticmethod
    async def save_output_to_neo4j(file_path: str):
        """
        Reads a file containing Cypher queries and executes them against a Neo4j database.

        Args:
            neo4j_uri (str): The URL of the Neo4j instance (e.g., 'bolt://localhost:7687')
            file_path (str): The path to the file containing Cypher queries.
        """

        neo4j_uri = os.getenv("NEO4J_URI")
        neo4j_user = os.getenv("NEO4J_USERNAME")
        neo4j_password = os.getenv("NEO4J_PASSWORD")
        if not neo4j_uri:
            logger.error("NEO4J_URI environment variable is not set.")
            return
        if not neo4j_user:
            logger.error("NEO4J_USERNAME environment variable is not set.")
            return
        if not neo4j_password:
            logger.error("NEO4J_PASSWORD environment variable is not set.")
            return

        try:
            driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
            driver.verify_connectivity()
            logger.info("Successfully connected to Neo4j.")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            return

        try:
            with driver.session() as session:
                with open(file_path, "r", encoding="utf-8") as f:
                    query_buffer = []

                    for line in f:
                        stripped_line = line.strip()

                        if not stripped_line:
                            continue

                        query_buffer.append(line)

                        if stripped_line.endswith(";"):
                            full_query = "".join(query_buffer)

                            try:
                                session.run(full_query)
                                logger.debug(
                                    f"Successfully executed query:\n{full_query}"
                                )
                            except Exception as e:
                                logger.error(
                                    f"Error executing query chunk:\n{full_query}\nError: {e}"
                                )

                            query_buffer = []

        except FileNotFoundError:
            logger.error(f"The file at {file_path} was not found.")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
        finally:
            driver.close()
            logger.info("Neo4j connection closed.")
