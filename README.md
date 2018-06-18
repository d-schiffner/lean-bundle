# LEarning ANalytics Bundles with HDF5
Written by Daniel Schiffner and Marcel Ritter

## Layout
* `/User/Authority/Id/Configuration/Timestamp/Fibers`
* `/LearningObjects/Authority/Id/Timestamp/Fibers`
* `/Interactions/Publisher/Name|Recipes/Fibers`

### Id
Ids are unique for a LEAN bundle, but do not need to be globally unique. These ids are taken from a id provider or defined when storing. If an existing id is referenced, the given entry is extended.

## Users
### Configuration
Generic information, on how the data was tracked
* Browser + Version
* System it was called in
* Timestamp default resolution (milliseconds)
* [Optional: Starting Learning Object]?

### Timestamp
Contains the timestamps for a specific configuration
* Measured using unix epoch (default: milliseconds)
* Represents the server storage time if no timestamp was given by the user (xAPI)

### Fibers for Users
Interaction + Object, Results, Tracking-Data, Attachments

Interactions cannot be separated from the object. Every learning experience is bound to a learning object. If not specific learning object is referenced, the containing learning object is used instead.

## Learning Objects
### Authority
It is required for a learning object, as it has to be created by someone. As labels, additional information can be provided.

### Timestamp
The versioning is done by timestamp, as for each LO, several variants may exist. A LO always needs to be referenced with a timestamp

### Fibers for Learning Objects
Metadata (Creator, Date, References, UsedBy), Aggregated LOs (Links)

## Interactions
### Publisher
The issuer/publisher of the named interaction. Uses mainly ADL

### Name | Recipes
Mostly standard xAPI verbs. To create aliases, just create a link.

A recipe may also be created, which represents a series of interactions that produce a result. The folder may contain several hdf5 filters and/or searches, to apply the desired result.

### Fibers for Interactions
xAPI verb, Descriptions

## Questions
1. Is there a wildcard authority?  
   A: Yes, it is called `default` and does not have any labels
2. How to track a single session?
3. How to separate LearningObjects used in different aggregations?
4. How to track multiple users for a single LearningObject?
5. How to track multiple users for a LeaningObject aggregation?
6. What language is used for the recipes, when defining filters or searches?
7. Is it necessary to seprarate LO ids and timestamps? What are the benefits?
8. How is data sent to a LEAN bundle?
9. How is aggregated data being represented in the LEAN bundle?
10. Is it possible to remove sensitive information from a LEAN bundle?  
  A: Yes. There are several options. Starting from removing user information, up to applying jitter to mouse or touch interactions
11. Is the starting learning object required?
12. How is previously stored data imported into a LEAN bundle?
13. How are LO aggregates identified?
14. Is it necessary to rewrite all data in a new 'version' of a LO?