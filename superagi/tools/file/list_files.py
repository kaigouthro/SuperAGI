import os
from typing import Type

from pydantic import BaseModel, Field

from superagi.helper.resource_helper import ResourceHelper
from superagi.tools.base_tool import BaseTool
from superagi.models.agent import Agent


class ListFileInput(BaseModel):
    pass


class ListFileTool(BaseTool):
    """
    List File tool

    Attributes:
        name : The name.
        agent_id: The agent id.
        description : The description.
        args_schema : The args schema.
    """
    name: str = "List File"
    agent_id: int = None
    args_schema: Type[BaseModel] = ListFileInput
    description: str = "lists files in a directory recursively"

    def _execute(self):
        """
        Execute the list file tool.

        Args:
            directory : The directory to list files in.

        Returns:
            list of files in directory.
        """
        input_directory = ResourceHelper.get_root_input_dir()
        #output_directory = ResourceHelper.get_root_output_dir()
        if "{agent_id}" in input_directory:
            input_directory = ResourceHelper.get_formatted_agent_level_path(agent=Agent
                                                                            .get_agent_from_id(session=self
                                                                                               .toolkit_config.session,
                                                                                               agent_id=self.agent_id),
                                                                            path=input_directory)
        return self.list_files(input_directory)

    def list_files(self, directory):
        found_files = []
        for root, dirs, files in os.walk(directory):
            found_files.extend(
                file
                for file in files
                if not file.startswith(".") and "__pycache__" not in root
            )
        return found_files
