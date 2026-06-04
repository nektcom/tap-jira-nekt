"""Stream type classes for tap-jira."""

from __future__ import annotations

from functools import cached_property
from typing import Any, Mapping

import requests
from nekt_singer_sdk import typing as th
from nekt_singer_sdk.custom_logger import user_logger
from nekt_singer_sdk.pagination import JSONPathPaginator

from tap_jira_nekt.client import JiraStream


class IssueStream(JiraStream):
    name = "issues"
    path = "/search/jql"
    primary_keys = ["id"]
    replication_key = "updated"
    records_jsonpath = "$[issues][*]"

    @cached_property
    def schema(self) -> dict:
        custom_field_props: list[th.Property] = []
        try:
            response = requests.get(
                f"https://{self.config['domain']}:443/rest/api/3/field",
                auth=(self.config["email"], self.config["api_token"]),
                timeout=30,
            )
            response.raise_for_status()
            jira_to_th: dict = {"number": th.NumberType, "boolean": th.BooleanType}
            for field in response.json():
                if not field.get("custom"):
                    continue
                field_id = field.get("id", "")
                field_type = field.get("schema", {}).get("type", "")
                custom_field_props.append(
                    th.Property(
                        field_id,
                        jira_to_th.get(field_type, th.StringType),
                        description=field.get("name", field_id),
                    )
                )
        except Exception as e:
            user_logger.warning(f"[{self.name}] Could not fetch custom fields: {e}")

        return th.PropertiesList(
        th.Property("expand", th.StringType, description="Expandable fields included in the response."),
        th.Property("id", th.StringType, description="Unique identifier of the record."),
        th.Property("self", th.StringType, description="URL of the resource."),
        th.Property("key", th.StringType, description="Unique key of the record."),
        th.Property(
            "fields",
            th.ObjectType(
                th.Property("description", th.StringType, description="Description of the record."),
                th.Property("created", th.DateTimeType, description="Timestamp when the record was created."),
                th.Property("updated", th.DateTimeType, description="Timestamp when the record was last updated."),
                th.Property(
                    "status_category",
                    th.ObjectType(
                        th.Property("color_name", th.StringType, description="Color name of the record."),
                        th.Property("id", th.IntegerType, description="Unique identifier of the record."),
                        th.Property("key", th.StringType, description="Unique key of the record."),
                        th.Property("name", th.StringType, description="Name of the record."),
                        th.Property("self", th.StringType, description="URL of the resource."),
                    ),
                
                    description="Status category details for the record."),
                th.Property("statuscategorychangedate", th.StringType, description="Statuscategorychangedate of the record."),
                th.Property(
                    "issuetype",
                    th.ObjectType(
                        th.Property("self", th.StringType, description="URL of the resource."),
                        th.Property("id", th.StringType, description="Unique identifier of the record."),
                        th.Property("description", th.StringType, description="Description of the record."),
                        th.Property("icon_url", th.StringType, description="URL of the icon."),
                        th.Property("name", th.StringType, description="Name of the record."),
                        th.Property("subtask", th.BooleanType, description="Subtask of the record."),
                        th.Property("avatar_id", th.IntegerType, description="Identifier of the associated avatar."),
                        th.Property("entity_id", th.StringType, description="Identifier of the associated entity."),
                        th.Property("hierarchy_level", th.IntegerType, description="Hierarchy level of the record."),
                    ),
                
                    description="Issuetype of the record."),
                th.Property(
                    "parent",
                    th.ObjectType(
                        th.Property("id", th.StringType, description="Unique identifier of the record."),
                        th.Property("key", th.StringType, description="Unique key of the record."),
                        th.Property("self", th.StringType, description="URL of the resource."),
                        th.Property(
                            "fields",
                            th.ObjectType(
                                th.Property("summary", th.StringType, description="Short summary of the record."),
                                th.Property("created", th.DateTimeType, description="Timestamp when the record was created."),
                                th.Property("updated", th.DateTimeType, description="Timestamp when the record was last updated."),
                                th.Property(
                                    "status",
                                    th.ObjectType(
                                        th.Property("description", th.StringType, description="Description of the record."),
                                        th.Property("icon_url", th.StringType, description="URL of the icon."),
                                        th.Property("id", th.StringType, description="Unique identifier of the record."),
                                        th.Property("name", th.StringType, description="Name of the record."),
                                        th.Property("self", th.StringType, description="URL of the resource."),
                                        th.Property(
                                            "status_category",
                                            th.ObjectType(
                                                th.Property("color_name", th.StringType, description="Color name of the record."),
                                                th.Property("id", th.IntegerType, description="Unique identifier of the record."),
                                                th.Property("key", th.StringType, description="Unique key of the record."),
                                                th.Property("name", th.StringType, description="Name of the record."),
                                                th.Property("self", th.StringType, description="URL of the resource."),
                                            ),
                                        
                                            description="Status category details for the record."),
                                    ),
                                
                                    description="Current status of the record."),
                                th.Property(
                                    "priority",
                                    th.ObjectType(
                                        th.Property("self", th.StringType, description="URL of the resource."),
                                        th.Property("icon_url", th.StringType, description="URL of the icon."),
                                        th.Property("name", th.StringType, description="Name of the record."),
                                        th.Property("id", th.StringType, description="Unique identifier of the record."),
                                    ),
                                
                                    description="Priority of the record."),
                                th.Property(
                                    "issuetype",
                                    th.ObjectType(
                                        th.Property("self", th.StringType, description="URL of the resource."),
                                        th.Property("id", th.StringType, description="Unique identifier of the record."),
                                        th.Property("description", th.StringType, description="Description of the record."),
                                        th.Property("icon_url", th.StringType, description="URL of the icon."),
                                        th.Property("name", th.StringType, description="Name of the record."),
                                        th.Property("subtask", th.BooleanType, description="Subtask of the record."),
                                        th.Property("avatar_id", th.IntegerType, description="Identifier of the associated avatar."),
                                        th.Property("entity_id", th.StringType, description="Identifier of the associated entity."),
                                        th.Property("hierarchy_level", th.IntegerType, description="Hierarchy level of the record."),
                                    ),
                                
                                    description="Issuetype of the record."),
                            ),
                        
                            description="Fields of the record."),
                    ),
                
                    description="Parent of the record."),
                th.Property("timespent", th.IntegerType, description="Timespent of the record."),
                th.Property(
                    "project",
                    th.ObjectType(
                        th.Property("self", th.StringType, description="URL of the resource."),
                        th.Property("id", th.StringType, description="Unique identifier of the record."),
                        th.Property("key", th.StringType, description="Unique key of the record."),
                        th.Property("name", th.StringType, description="Name of the record."),
                        th.Property("project_type_key", th.StringType, description="Project type key of the record."),
                        th.Property("simplified", th.BooleanType, description="Simplified of the record."),
                        th.Property(
                            "avatar_urls",
                            th.ObjectType(
                                th.Property("48x48", th.StringType, description="48x48 of the record."),
                                th.Property("24x24", th.StringType, description="24x24 of the record."),
                                th.Property("16x16", th.StringType, description="16x16 of the record."),
                                th.Property("32x32", th.StringType, description="32x32 of the record."),
                            ),
                        
                            description="URLs related to the avatar."),
                    ),
                
                    description="Project of the record."),
                th.Property(
                    "fix_versions",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("id", th.StringType, description="Unique identifier of the record."),
                            th.Property("archived", th.BooleanType, description="Archived of the record."),
                            th.Property("name", th.StringType, description="Name of the record."),
                            th.Property("released", th.BooleanType, description="Released of the record."),
                            th.Property("self", th.StringType, description="URL of the resource."),
                        ),
                    ),
                
                    description="Fix versions of the record."),
                th.Property("aggregatetimespent", th.IntegerType, description="Aggregatetimespent of the record."),
                th.Property(
                    "resolution",
                    th.ObjectType(
                        th.Property("description", th.StringType, description="Description of the record."),
                        th.Property("id", th.StringType, description="Unique identifier of the record."),
                        th.Property("name", th.StringType, description="Name of the record."),
                        th.Property("self", th.StringType, description="URL of the resource."),
                    ),
                
                    description="Resolution of the record."),
                th.Property("resolutiondate", th.StringType, description="Resolutiondate of the record."),
                th.Property("workratio", th.IntegerType, description="Workratio of the record."),
                th.Property(
                    "watches",
                    th.ObjectType(
                        th.Property("self", th.StringType, description="URL of the resource."),
                        th.Property("watch_count", th.IntegerType, description="Watch count of the record."),
                        th.Property("is_watching", th.BooleanType, description="Indicates whether the record is watching."),
                    ),
                
                    description="Watches of the record."),
                th.Property("issuerestriction", th.StringType, description="Issuerestriction of the record."),
                th.Property("last_viewed", th.StringType, description="Last viewed of the record."),
                th.Property(
                    "priority",
                    th.ObjectType(
                        th.Property("self", th.StringType, description="URL of the resource."),
                        th.Property("icon_url", th.StringType, description="URL of the icon."),
                        th.Property("name", th.StringType, description="Name of the record."),
                        th.Property("id", th.StringType, description="Unique identifier of the record."),
                    ),
                
                    description="Priority of the record."),
                th.Property("labels", th.ArrayType(th.StringType), description="Labels of the record."),
                th.Property("timeestimate", th.IntegerType, description="Timeestimate of the record."),
                th.Property("aggregatetimeoriginalestimate", th.IntegerType, description="Aggregatetimeoriginalestimate of the record."),
                th.Property("versions", th.ArrayType(th.StringType), description="Versions of the record."),
                th.Property(
                    "issuelinks",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("id", th.StringType, description="Unique identifier of the record."),
                            th.Property(
                                "outward_issue",
                                th.ObjectType(
                                    th.Property(
                                        "fields",
                                        th.ObjectType(
                                            th.Property(
                                                "issuetype",
                                                th.ObjectType(
                                                    th.Property("avatar_id", th.IntegerType, description="Identifier of the associated avatar."),
                                                    th.Property("description", th.StringType, description="Description of the record."),
                                                    th.Property("entity_id", th.StringType, description="Identifier of the associated entity."),
                                                    th.Property(
                                                        "hierarchy_level",
                                                        th.IntegerType,
                                                    
                                                        description="Hierarchy level of the record."),
                                                    th.Property("icon_url", th.StringType, description="URL of the icon."),
                                                    th.Property("id", th.StringType, description="Unique identifier of the record."),
                                                    th.Property("name", th.StringType, description="Name of the record."),
                                                    th.Property("self", th.StringType, description="URL of the resource."),
                                                    th.Property("subtask", th.BooleanType, description="Subtask of the record."),
                                                ),
                                            
                                                description="Issuetype of the record."),
                                            th.Property(
                                                "priority",
                                                th.ObjectType(
                                                    th.Property("icon_url", th.StringType, description="URL of the icon."),
                                                    th.Property("id", th.StringType, description="Unique identifier of the record."),
                                                    th.Property("name", th.StringType, description="Name of the record."),
                                                    th.Property("self", th.StringType, description="URL of the resource."),
                                                ),
                                            
                                                description="Priority of the record."),
                                            th.Property(
                                                "status",
                                                th.ObjectType(
                                                    th.Property("description", th.StringType, description="Description of the record."),
                                                    th.Property("icon_url", th.StringType, description="URL of the icon."),
                                                    th.Property("id", th.StringType, description="Unique identifier of the record."),
                                                    th.Property("name", th.StringType, description="Name of the record."),
                                                    th.Property("self", th.StringType, description="URL of the resource."),
                                                    th.Property(
                                                        "status_category",
                                                        th.ObjectType(
                                                            th.Property(
                                                                "color_name",
                                                                th.StringType,
                                                            
                                                                description="Color name of the record."),
                                                            th.Property("id", th.IntegerType, description="Unique identifier of the record."),
                                                            th.Property("key", th.StringType, description="Unique key of the record."),
                                                            th.Property(
                                                                "name",
                                                                th.StringType,
                                                            
                                                                description="Name of the record."),
                                                            th.Property(
                                                                "self",
                                                                th.StringType,
                                                            
                                                                description="URL of the resource."),
                                                        ),
                                                    
                                                        description="Status category details for the record."),
                                                ),
                                            
                                                description="Current status of the record."),
                                            th.Property("summary", th.StringType, description="Short summary of the record."),
                                        ),
                                    
                                        description="Fields of the record."),
                                    th.Property("id", th.StringType, description="Unique identifier of the record."),
                                    th.Property("key", th.StringType, description="Unique key of the record."),
                                    th.Property("self", th.StringType, description="URL of the resource."),
                                ),
                            
                                description="Outward issue of the record."),
                            th.Property(
                                "inward_issue",
                                th.ObjectType(
                                    th.Property(
                                        "fields",
                                        th.ObjectType(
                                            th.Property(
                                                "issuetype",
                                                th.ObjectType(
                                                    th.Property("avatar_id", th.IntegerType, description="Identifier of the associated avatar."),
                                                    th.Property("description", th.StringType, description="Description of the record."),
                                                    th.Property("entity_id", th.StringType, description="Identifier of the associated entity."),
                                                    th.Property(
                                                        "hierarchy_level",
                                                        th.IntegerType,
                                                    
                                                        description="Hierarchy level of the record."),
                                                    th.Property("icon_url", th.StringType, description="URL of the icon."),
                                                    th.Property("id", th.StringType, description="Unique identifier of the record."),
                                                    th.Property("name", th.StringType, description="Name of the record."),
                                                    th.Property("self", th.StringType, description="URL of the resource."),
                                                    th.Property("subtask", th.BooleanType, description="Subtask of the record."),
                                                ),
                                            
                                                description="Issuetype of the record."),
                                            th.Property(
                                                "priority",
                                                th.ObjectType(
                                                    th.Property("icon_url", th.StringType, description="URL of the icon."),
                                                    th.Property("id", th.StringType, description="Unique identifier of the record."),
                                                    th.Property("name", th.StringType, description="Name of the record."),
                                                    th.Property("self", th.StringType, description="URL of the resource."),
                                                ),
                                            
                                                description="Priority of the record."),
                                            th.Property(
                                                "status",
                                                th.ObjectType(
                                                    th.Property("description", th.StringType, description="Description of the record."),
                                                    th.Property("icon_url", th.StringType, description="URL of the icon."),
                                                    th.Property("id", th.StringType, description="Unique identifier of the record."),
                                                    th.Property("name", th.StringType, description="Name of the record."),
                                                    th.Property("self", th.StringType, description="URL of the resource."),
                                                    th.Property(
                                                        "statusCategory",
                                                        th.ObjectType(
                                                            th.Property(
                                                                "color_name",
                                                                th.StringType,
                                                            
                                                                description="Color name of the record."),
                                                            th.Property("id", th.IntegerType, description="Unique identifier of the record."),
                                                            th.Property("key", th.StringType, description="Unique key of the record."),
                                                            th.Property(
                                                                "name",
                                                                th.StringType,
                                                            
                                                                description="Name of the record."),
                                                            th.Property(
                                                                "self",
                                                                th.StringType,
                                                            
                                                                description="URL of the resource."),
                                                        ),
                                                    
                                                        description="Status category details for the record."),
                                                ),
                                            
                                                description="Current status of the record."),
                                            th.Property("summary", th.StringType, description="Short summary of the record."),
                                        ),
                                    
                                        description="Fields of the record."),
                                    th.Property("id", th.StringType, description="Unique identifier of the record."),
                                    th.Property("key", th.StringType, description="Unique key of the record."),
                                    th.Property("self", th.StringType, description="URL of the resource."),
                                ),
                            
                                description="Inward issue of the record."),
                            th.Property("self", th.StringType, description="URL of the resource."),
                            th.Property(
                                "type",
                                th.ObjectType(
                                    th.Property("id", th.StringType, description="Unique identifier of the record."),
                                    th.Property("inward", th.StringType, description="Inward of the record."),
                                    th.Property("name", th.StringType, description="Name of the record."),
                                    th.Property("outward", th.StringType, description="Outward of the record."),
                                    th.Property("self", th.StringType, description="URL of the resource."),
                                ),
                            
                                description="Type classification of the record."),
                        ),
                    ),
                
                    description="Issuelinks of the record."),
                th.Property(
                    "assignee",
                    th.ObjectType(
                        th.Property("self", th.StringType, description="URL of the resource."),
                        th.Property("account_id", th.StringType, description="Identifier of the associated account."),
                        th.Property(
                            "avatar_urls",
                            th.ObjectType(
                                th.Property("48x48", th.StringType, description="48x48 of the record."),
                                th.Property("24x24", th.StringType, description="24x24 of the record."),
                                th.Property("16x16", th.StringType, description="16x16 of the record."),
                                th.Property("32x32", th.StringType, description="32x32 of the record."),
                            ),
                        
                            description="URLs related to the avatar."),
                        th.Property("display_name", th.StringType, description="Display name of the record."),
                        th.Property("active", th.BooleanType, description="Indicates whether the record is active."),
                        th.Property("time_zone", th.StringType, description="Time zone of the record."),
                        th.Property("account_type", th.StringType, description="Account type of the record."),
                        th.Property("email_address", th.StringType, description="Email address of the record."),
                    ),
                
                    description="Assignee of the record."),
                th.Property(
                    "status",
                    th.ObjectType(
                        th.Property("self", th.StringType, description="URL of the resource."),
                        th.Property("description", th.StringType, description="Description of the record."),
                        th.Property("icon_url", th.StringType, description="URL of the icon."),
                        th.Property("name", th.StringType, description="Name of the record."),
                        th.Property("id", th.StringType, description="Unique identifier of the record."),
                        th.Property(
                            "status_category",
                            th.ObjectType(
                                th.Property("self", th.StringType, description="URL of the resource."),
                                th.Property("id", th.IntegerType, description="Unique identifier of the record."),
                                th.Property("key", th.StringType, description="Unique key of the record."),
                                th.Property("color_name", th.StringType, description="Color name of the record."),
                                th.Property("name", th.StringType, description="Name of the record."),
                            ),
                        
                            description="Status category details for the record."),
                    ),
                
                    description="Current status of the record."),
                th.Property(
                    "components",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("self", th.StringType, description="URL of the resource."),
                            th.Property("id", th.StringType, description="Unique identifier of the record."),
                            th.Property("name", th.StringType, description="Name of the record."),
                        ),
                    ),
                
                    description="Components of the record."),
                th.Property("timeoriginalestimate", th.IntegerType, description="Timeoriginalestimate of the record."),
                th.Property("timetracking", th.StringType, description="Timetracking of the record."),
                th.Property("security", th.StringType, description="Security of the record."),
                th.Property("aggregatetimeestimate", th.IntegerType, description="Aggregatetimeestimate of the record."),
                th.Property("attachment", th.ArrayType(th.StringType), description="Attachment of the record."),
                th.Property("summary", th.StringType, description="Short summary of the record."),
                th.Property(
                    "creator",
                    th.ObjectType(
                        th.Property("self", th.StringType, description="URL of the resource."),
                        th.Property("account_id", th.StringType, description="Identifier of the associated account."),
                        th.Property("email_address", th.StringType, description="Email address of the record."),
                        th.Property(
                            "avatar_urls",
                            th.ObjectType(
                                th.Property("48x48", th.StringType, description="48x48 of the record."),
                                th.Property("24x24", th.StringType, description="24x24 of the record."),
                                th.Property("16x16", th.StringType, description="16x16 of the record."),
                                th.Property("32x32", th.StringType, description="32x32 of the record."),
                            ),
                        
                            description="URLs related to the avatar."),
                        th.Property("display_name", th.StringType, description="Display name of the record."),
                        th.Property("active", th.BooleanType, description="Indicates whether the record is active."),
                        th.Property("time_zone", th.StringType, description="Time zone of the record."),
                        th.Property("account_type", th.StringType, description="Account type of the record."),
                    ),
                
                    description="Creator of the record."),
                th.Property(
                    "subtasks",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("id", th.StringType, description="Unique identifier of the record."),
                            th.Property("key", th.StringType, description="Unique key of the record."),
                            th.Property("self", th.StringType, description="URL of the resource."),
                            th.Property(
                                "fields",
                                th.ObjectType(
                                    th.Property("summary", th.StringType, description="Short summary of the record."),
                                    th.Property(
                                        "status",
                                        th.ObjectType(
                                            th.Property("self", th.StringType, description="URL of the resource."),
                                            th.Property("description", th.StringType, description="Description of the record."),
                                            th.Property("icon_url", th.StringType, description="URL of the icon."),
                                            th.Property("name", th.StringType, description="Name of the record."),
                                            th.Property("id", th.StringType, description="Unique identifier of the record."),
                                            th.Property(
                                                "statusCategory",
                                                th.ObjectType(
                                                    th.Property("self", th.StringType, description="URL of the resource."),
                                                    th.Property("id", th.IntegerType, description="Unique identifier of the record."),
                                                    th.Property("key", th.StringType, description="Unique key of the record."),
                                                    th.Property("color_name", th.StringType, description="Color name of the record."),
                                                    th.Property("name", th.StringType, description="Name of the record."),
                                                ),
                                            
                                                description="Status category details for the record."),
                                        ),
                                    
                                        description="Current status of the record."),
                                    th.Property(
                                        "priority",
                                        th.ObjectType(
                                            th.Property("self", th.StringType, description="URL of the resource."),
                                            th.Property("icon_url", th.StringType, description="URL of the icon."),
                                            th.Property("name", th.StringType, description="Name of the record."),
                                            th.Property("id", th.StringType, description="Unique identifier of the record."),
                                        ),
                                    
                                        description="Priority of the record."),
                                    th.Property(
                                        "issuetype",
                                        th.ObjectType(
                                            th.Property("self", th.StringType, description="URL of the resource."),
                                            th.Property("id", th.StringType, description="Unique identifier of the record."),
                                            th.Property("description", th.StringType, description="Description of the record."),
                                            th.Property("icon_url", th.StringType, description="URL of the icon."),
                                            th.Property("name", th.StringType, description="Name of the record."),
                                            th.Property("subtask", th.BooleanType, description="Subtask of the record."),
                                            th.Property("avatar_id", th.IntegerType, description="Identifier of the associated avatar."),
                                            th.Property("entity_id", th.StringType, description="Identifier of the associated entity."),
                                            th.Property("hierarchy_level", th.IntegerType, description="Hierarchy level of the record."),
                                        ),
                                    
                                        description="Issuetype of the record."),
                                ),
                            
                                description="Fields of the record."),
                        ),
                    ),
                
                    description="Subtasks of the record."),
                th.Property(
                    "reporter",
                    th.ObjectType(
                        th.Property("self", th.StringType, description="URL of the resource."),
                        th.Property("account_id", th.StringType, description="Identifier of the associated account."),
                        th.Property("email_address", th.StringType, description="Email address of the record."),
                        th.Property(
                            "avatar_urls",
                            th.ObjectType(
                                th.Property("48x48", th.StringType, description="48x48 of the record."),
                                th.Property("24x24", th.StringType, description="24x24 of the record."),
                                th.Property("16x16", th.StringType, description="16x16 of the record."),
                                th.Property("32x32", th.StringType, description="32x32 of the record."),
                            ),
                        
                            description="URLs related to the avatar."),
                        th.Property("display_name", th.StringType, description="Display name of the record."),
                        th.Property("active", th.BooleanType, description="Indicates whether the record is active."),
                        th.Property("time_zone", th.StringType, description="Time zone of the record."),
                        th.Property("account_type", th.StringType, description="Account type of the record."),
                    ),
                
                    description="Reporter of the record."),
                th.Property(
                    "aggregateprogress",
                    th.ObjectType(
                        th.Property("progress", th.IntegerType, description="Progress of the record."),
                        th.Property("total", th.IntegerType, description="Monetary value associated with the record."),
                        th.Property("percent", th.IntegerType, description="Percent of the record."),
                    ),
                
                    description="Aggregateprogress of the record."),
                th.Property(
                    "environment",
                    th.ObjectType(
                        th.Property("type", th.StringType, description="Type classification of the record."),
                        th.Property(
                            "content",
                            th.ArrayType(
                                th.ObjectType(
                                    th.Property(
                                        "content",
                                        th.ArrayType(
                                            th.ObjectType(
                                                th.Property("text", th.StringType, description="Text of the record."),
                                                th.Property("type", th.StringType, description="Type classification of the record."),
                                            ),
                                        ),
                                    
                                        description="Content of the record."),
                                    th.Property("type", th.StringType, description="Type classification of the record."),
                                ),
                            ),
                        
                            description="Content of the record."),
                        th.Property("text", th.StringType, description="Text of the record."),
                        th.Property("version", th.IntegerType, description="Version of the record."),
                    ),
                
                    description="Environment of the record."),
                th.Property("duedate", th.StringType, description="Duedate of the record."),
                th.Property(
                    "progress",
                    th.ObjectType(
                        th.Property("progress", th.IntegerType, description="Progress of the record."),
                        th.Property("total", th.IntegerType, description="Monetary value associated with the record."),
                    ),
                
                    description="Progress of the record."),
                th.Property("comment", th.StringType, description="Comment of the record."),
                th.Property(
                    "votes",
                    th.ObjectType(
                        th.Property("self", th.StringType, description="URL of the resource."),
                        th.Property("votes", th.IntegerType, description="Votes of the record."),
                        th.Property("has_voted", th.BooleanType, description="Has voted of the record."),
                    ),
                
                    description="Votes of the record."),
                th.Property("worklog", th.StringType, description="Worklog of the record."),
                th.Property("key", th.StringType, description="Unique key of the record."),
                th.Property("id", th.IntegerType, description="Unique identifier of the record."),
                th.Property("editmeta", th.StringType, description="Editmeta of the record."),
                th.Property("histories", th.StringType, description="Histories of the record."),
                *custom_field_props,
            ),

            description="Fields of the record."),
        th.Property("created", th.DateTimeType, description="Timestamp when the record was created."),
        th.Property("updated", th.DateTimeType, description="Timestamp when the record was last updated."),
    ).to_dict()

    def get_new_paginator(self) -> JSONPathPaginator:
        return JSONPathPaginator(jsonpath="$.nextPageToken")

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:
        """Return a dictionary of query parameters."""
        params: dict = {}
        params["maxResults"] = 100
        params["fields"] = "*all"

        jql: list[str] = []

        if next_page_token:
            params["nextPageToken"] = next_page_token

        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        jql.append(f"updated>='{self.get_starting_timestamp(context).strftime('%Y/%m/%d %H:%M')}'")

        # Add project filter if configured
        project_keys = self.config.get("project_keys")
        if project_keys:
            project_filter = " OR ".join([f'project = "{key}"' for key in project_keys])
            jql.append(f"({project_filter})")

        if base_jql := self.config.get("stream_options", {}).get("issues", {}).get("jql"):
            jql.append(f"({base_jql})")

        if jql:
            params["jql"] = " and ".join(jql)

        return params

    def validate_response(self, response: requests.Response) -> None:
        return super().validate_response(response)

    def post_process(self, row: dict[str, Any], context: Mapping[str, Any] | None = None) -> dict | None:
        new_row = row
        new_row["created"] = row["fields"]["created"]
        new_row["updated"] = row["fields"]["updated"]
        return super().post_process(new_row, context)

    def get_child_context(self, record: dict, context: dict | None) -> dict:  # noqa: ARG002
        """Return a context dictionary for child streams."""
        return {"issue_id": record["id"]}
